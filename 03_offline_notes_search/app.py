
import sys
import re
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import Store, form, heading, note, table, run


store = Store(
    Path(__file__).with_name("data.json"),
    {"folder": "", "history": []}
)

# Cached documents and word-to-document index
index_cache = {}


def get_index(folder):
    """Load notes and build an inverted index, reusing it when unchanged."""
    root = Path(folder).expanduser().resolve()

    if not root.is_dir():
        raise ValueError("Enter an existing notes folder.")

    paths = sorted(root.glob("*.txt"))

    signature = tuple(
        (str(path), path.stat().st_mtime_ns, path.stat().st_size)
        for path in paths
    )

    cache_key = str(root)

    if cache_key in index_cache:
        cached_signature, cached_data = index_cache[cache_key]
        if cached_signature == signature:
            return cached_data

    documents = {}
    inverted_index = {}

    for path in paths:
        text = path.read_text(encoding="utf-8")
        tokens = re.findall(r"\w+", text.lower())

        documents[path.name] = {
            "text": text,
            "lower": text.lower(),
            "tokens": tokens
        }

        # Each word maps to the documents containing it.
        for word in set(tokens):
            inverted_index.setdefault(word, set()).add(path.name)

    data = {
        "documents": documents,
        "index": inverted_index
    }

    index_cache[cache_key] = (signature, data)
    return data


def prepare_query(query):
    query = query.strip().lower()
    words = list(dict.fromkeys(re.findall(r"\w+", query)))

    if not words:
        raise ValueError("Enter a word or phrase.")

    return query, words


def make_result(filename, score, reason, position, text):
    start = max(0, position - 40)
    snippet = text[start:start + 180].replace("\n", " ")

    return [filename, score, reason, snippet]


def search_scan(folder, query, mode):
    """Reference-style search: scan every note for each query."""
    root = Path(folder).expanduser().resolve()

    if not root.is_dir():
        raise ValueError("Enter an existing notes folder.")

    query, words = prepare_query(query)
    results = []

    for path in sorted(root.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        tokens = re.findall(r"\w+", lower)

        if mode == "Exact phrase":
            score = lower.count(query)
            reason = f"Phrase appears {score} times"
            position = lower.find(query)

        else:
            counts = {word: tokens.count(word) for word in words}
            matched = sum(count > 0 for count in counts.values())
            total = sum(counts.values())

            if mode == "All words" and matched != len(words):
                continue

            if mode not in ["Keywords", "All words"]:
                raise ValueError("Select a valid search mode.")

            score = matched * 100 + total

            if mode == "Keywords":
                reason = (
                    f"{matched}/{len(words)} words matched; "
                    f"{total} occurrences"
                )
            else:
                reason = (
                    f"All {len(words)} query words matched; "
                    f"{total} occurrences"
                )

            positions = [
                match.start()
                for match in re.finditer(r"\w+", lower)
                if match.group() in words
            ]
            position = min(positions) if positions else -1

        if score > 0:
            results.append(
                make_result(
                    path.name, score, reason, position, text
                )
            )

    return sorted(results, key=lambda row: (-row[1], row[0]))


def search_indexed(folder, query, mode):
    """Search using the word-to-document index."""
    if mode == "Exact phrase":
        # A word index cannot directly verify phrase order.
        return search_scan(folder, query, mode)

    query, words = prepare_query(query)
    data = get_index(folder)
    documents = data["documents"]
    inverted_index = data["index"]

    if mode == "Keywords":
        candidate_names = set()
        for word in words:
            candidate_names.update(inverted_index.get(word, set()))

    elif mode == "All words":
        word_sets = [
            inverted_index.get(word, set()) for word in words
        ]

        if not word_sets:
            candidate_names = set()
        else:
            candidate_names = set.intersection(
                *(set(names) for names in word_sets)
            )

    else:
        raise ValueError("Select a valid search mode.")

    results = []

    for filename in sorted(candidate_names):
        document = documents[filename]
        text = document["text"]
        lower = document["lower"]
        tokens = document["tokens"]

        counts = {word: tokens.count(word) for word in words}
        matched = sum(count > 0 for count in counts.values())
        total = sum(counts.values())

        if mode == "All words" and matched != len(words):
            continue

        score = matched * 100 + total

        if mode == "Keywords":
            reason = (
                f"{matched}/{len(words)} words matched; "
                f"{total} occurrences"
            )
        else:
            reason = (
                f"All {len(words)} query words matched; "
                f"{total} occurrences"
            )

        positions = [
            match.start()
            for match in re.finditer(r"\w+", lower)
            if match.group() in words
        ]
        position = min(positions) if positions else -1

        results.append(
            make_result(
                filename, score, reason, position, text
            )
        )

    return sorted(results, key=lambda row: (-row[1], row[0]))


def benchmark(folder, query, mode, repetitions=100):
    """Compare repeated scan searches and indexed searches."""
    if mode == "Exact phrase":
        return [
            ["Scan search", "Not measured"],
            ["Indexed search", "Not applicable to exact phrases"]
        ]

    # Build the index before timing so index construction is not
    # counted as part of each repeated indexed search.
    get_index(folder)

    start = time.perf_counter()
    for _ in range(repetitions):
        search_scan(folder, query, mode)
    scan_time = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(repetitions):
        search_indexed(folder, query, mode)
    indexed_time = time.perf_counter() - start

    return [
        [
            f"Scan approach ({repetitions} searches)",
            f"{scan_time:.6f} seconds"
        ],
        [
            f"Indexed approach ({repetitions} searches)",
            f"{indexed_time:.6f} seconds"
        ],
        [
            "Scan time per search",
            f"{scan_time / repetitions:.8f} seconds"
        ],
        [
            "Indexed time per search",
            f"{indexed_time / repetitions:.8f} seconds"
        ]
    ]


def view():
    out = note(
        "Search UTF-8 .txt files directly inside the selected folder. "
        "Keywords matches any query word. All words requires every "
        "distinct query word. Exact phrase searches the complete phrase. "
        "The performance comparison uses 100 repeated searches."
    )

    out += form(
        "search",
        [
            (
                "folder",
                "Full notes folder path",
                "text",
                store.data["folder"]
            ),
            (
                "query",
                "Search words or phrase",
                "text",
                "dynamic programming"
            ),
            (
                "mode",
                "Search mode",
                "select",
                ["Keywords", "Exact phrase", "All words"]
            )
        ],
        "Search notes"
    )

    out += heading("Recent searches")
    out += table(["Query", "Mode"], store.data["history"])

    return out


def handle(data):
    if data["action"] != "search":
        raise ValueError("Unknown action.")

    if data["mode"] not in [
        "Keywords", "Exact phrase", "All words"
    ]:
        raise ValueError("Select a valid search mode.")

    folder = data["folder"]
    query = data["query"]
    mode = data["mode"]

    # Show the search results from the indexed approach.
    results = search_indexed(folder, query, mode)

    store.data["folder"] = folder
    store.data["history"] = [
        [query, mode]
    ] + store.data["history"][:9]
    store.save()

    out = heading("Search results")
    out += table(
        ["File", "Score", "Why this rank", "Snippet"],
        results
    )

    # Demonstrate that both approaches return the same results.
    if mode != "Exact phrase":
        scan_results = search_scan(folder, query, mode)
        same_results = scan_results == results

        out += heading("Correctness check")
        out += table(
            ["Check", "Result"],
            [[
                "Scan and index results match",
                "Yes" if same_results else "No"
            ]]
        )

    out += heading("Repeated-search performance")
    timings = benchmark(folder, query, mode)
    out += table(["Approach", "Time"], timings)

    if mode == "Exact phrase":
        out += note(
            "Exact phrase search uses the scan approach because "
            "the word-to-document index does not preserve word order."
        )

    return out


if __name__ == "__main__":
    run("Offline Notes Search Engine", view, handle)
