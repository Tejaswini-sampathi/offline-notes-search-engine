# 🔎 Offline Notes Search Engine

### Your study notes. One search away.

A lightweight, Python-based search engine that helps students find information across local study notes — without depending on an internet connection.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Search-Offline-success" alt="Offline Search">
  <img src="https://img.shields.io/badge/Domain-Data%20Structures-orange" alt="Data Structures">
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen" alt="Project Status">
</p>

---

## ✨ What makes it useful?

Imagine having hundreds of pages of study notes. Instead of opening each file individually, search for a topic and find the relevant documents in seconds.

This project explores how search algorithms and data structures can make that process more efficient.

## 🚀 Features

| Feature | Description |
|---|---|
| 🔑 Keyword Search | Finds documents containing one or more query words. |
| 💬 Exact Phrase Search | Searches for a phrase in the same word order. |
| 🧩 All Words Search | Returns documents containing every distinct query word. |
| 📊 Relevance Ranking | Orders results using the implemented scoring method. |
| 📝 Text Snippets | Displays useful excerpts from matching documents. |
| 🕘 Search History | Maintains recent searches using local application data. |
| ⚡ Inverted Index | Maps words to documents to narrow search candidates. |
| ⏱️ Performance Benchmark | Compares scan-based and indexed search across repeated queries. |
| 📵 Offline Search | Searches local notes without requiring internet access. |

## 🧠 Under the Hood

The project demonstrates two approaches to searching text documents.

### 1. Scan-Based Search

The program examines the documents and checks their contents against the search query.

**Idea:** Search through the available documents to identify matches.

### 2. Inverted Index

An inverted index stores a mapping from each word to the documents in which it appears.

Example:

```text
database  → {dbms.txt}
python    → {python.txt}
algorithm → {daa.txt}
```

When a query is entered, the index helps identify candidate documents without examining every document from scratch.

### 3. Performance Comparison

The application measures repeated searches using both approaches.

The comparison helps demonstrate how an inverted index can improve search efficiency when working with larger collections of notes. Actual results depend on document size, query terms, and system conditions.

## 🛠️ Tech Stack

- **Language:** Python
- **Data structures:** Dictionaries, sets, and lists
- **Text processing:** Regular expressions
- **File handling:** `pathlib` and standard Python file operations
- **Local data storage:** JSON
- **Version control:** Git and GitHub

## 📂 Project Structure

```text
03_offline_notes_search/
│
├── app.py
├── common.py
├── README.md
├── .gitignore
│
└── notes/
    ├── daa.txt
    ├── dbms.txt
    └── python.txt
```

**Generated locally:** `data.json` stores application data and is excluded from Git by `.gitignore`.

## ⚙️ Getting Started

### Prerequisites

- Python 3
- Git
- A web browser
- The project's required helper module

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Tejaswini-sampathi/offline-notes-search-engine.git
```

**2. Navigate to the project**

```bash
cd offline-notes-search-engine
```

**3. Run the application**

```bash
python app.py
```

On Windows, you can also try:

```powershell
py app.py
```

**4. Open the application**

Open the local URL displayed in the terminal in your browser.

**5. Select your notes folder**

Enter the full path to the `notes` directory when prompted by the interface.

> **Note:** The application imports `common.py`, so make sure that file is available in the expected location. If it is included inside the cloned project folder, the import path in `app.py` must match that structure.

## 🧪 Try It Out

Use these sample queries with the corresponding search modes:

| Search query | Mode | What it demonstrates |
|---|---|---|
| `dynamic programming` | Keywords | Matches documents containing either query word. |
| `database management` | All words | Requires both distinct words to occur. |
| `relational database` | Exact phrase | Checks for the phrase in the specified order. |
| `python functions` | Keywords | Searches for either term in the notes. |

The actual results depend on the contents of your notes files.

## 📈 Complexity and Performance

Let:

- \(T\) = total number of words in the documents.
- \(D\) = number of documents.
- \(Q\) = number of query words.

| Operation | General cost |
|---|---|
| Build inverted index | \(O(T)\) |
| Query-word dictionary lookups | Approximately \(O(Q)\), excluding result processing |
| Process candidate documents | Depends on the number and size of candidates |
| Scan-based search | Depends on the total text examined |

The index requires preprocessing and memory. Its advantage becomes more noticeable when the same collection is searched repeatedly. For a small collection, performance differences may be negligible.

## 🎓 What I Learned

Building this project helped me explore:

- How search algorithms retrieve information from text files.
- How dictionaries and sets support inverted indexing.
- How to compare two approaches using execution-time measurements.
- How to handle local files and JSON data in Python.
- How to organize source code and publish a project using Git and GitHub.

## 🔮 Future Improvements

- Support PDF and DOCX documents.
- Highlight matched words in results.
- Add subject and file-type filters.
- Improve ranking using TF-IDF or BM25.
- Support larger document collections.
- Add more search and indexing benchmarks.

## 👩‍💻 About the Developer

**Tejaswini Sampathi**

Computer Science and Engineering student interested in algorithms, data structures, and practical software development.

🔗 **GitHub:** [@Tejaswini-sampathi](https://github.com/Tejaswini-sampathi)

## 📜 License

Created for educational and academic purposes. An explicit open-source license can be added to define reuse and distribution permissions.

---

<p align="center">
  <i>Built to make finding knowledge in study notes simpler.</i>
</p>
