# 🧠 DocMind — RAG Chatbot with Live Web Search

A locally-hosted AI chatbot that answers questions from **your own documents** using Retrieval-Augmented Generation (RAG), with a hybrid fallback to **live web search** and general knowledge — so it never leaves you without an answer.

Built entirely with **open-source, local models** — no OpenAI key required for local use, no data ever leaves your machine.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Live Demo

🔗 **[Try DocMind Live](https://docmind-shlok.streamlit.app)**

> Deployed on Streamlit Community Cloud — chat with the demo document instantly, no setup required.

---

## 📸 Screenshots

### Chat Interface
![DocMind Chat Interface](https://github.com/user-attachments/assets/ffed847f-3918-406c-ad36-022411c05902)

### Question & Answer in Action
![DocMind Demo](https://github.com/user-attachments/assets/c9523f1b-83c9-42e1-b876-3ad656696565)

---

## 📖 Overview

Most chatbots either hallucinate answers or refuse to answer anything outside their training data. **DocMind** solves this with a 3-tier answering strategy:

1. **Your Documents (RAG)** — Checks your uploaded PDFs/text files first for a grounded, accurate answer.
2. **Live Web Search** — For time-sensitive queries (news, current events, prices), it pulls real-time results from the web.
3. **General Knowledge** — Falls back to the LLM's own trained knowledge for everything else.

This means you can ask it *anything* — from "What's in my resume?" to "Who is the current PM of India?" to "What is machine learning?" — and always get a direct, useful answer.

---

## ✨ Features

- 🔒 **100% Local & Private** — runs entirely on your machine via Ollama, no data sent to third parties
- 📄 **Document Q&A** — supports PDF and TXT files, chunked and embedded for semantic search
- 🌐 **Live Web Search Fallback** — automatically detects time-sensitive queries and fetches real-time info
- 🕒 **Accurate Real-Time Date/Time** — pulls exact date/time directly from a time API instead of guessing
- 💬 **Clean Chat UI** — built with Streamlit, includes chat history and source attribution
- ⚡ **Zero API Cost (local mode)** — no OpenAI/Anthropic key required; uses free local models via Ollama

---

## 🛠️ Tech Stack

| Component         | Technology                          |
|-------------------|--------------------------------------|
| LLM (chat)        | Llama 3.2 (via Ollama)              |
| Embeddings        | nomic-embed-text (via Ollama)       |
| Vector Database   | ChromaDB                            |
| Orchestration     | LangChain                           |
| Web Search        | DuckDuckGo Search (ddgs)            |
| UI                | Streamlit                           |
| Language          | Python 3.12                         |

---

## 🏗️ Architecture

```
                        ┌─────────────────┐
                        │   User Query     │
                        └────────┬─────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 ▼                                ▼
        ┌──────────────────┐           ┌────────────────────┐
        │  Vector Search     │           │  Live Web Search    │
        │  (ChromaDB +       │           │  (DuckDuckGo, only  │
        │   nomic-embed)     │           │   for time-sensitive │
        │                    │           │   queries)          │
        └─────────┬──────────┘           └──────────┬──────────┘
                  │                                  │
                  └───────────────┬──────────────────┘
                                  ▼
                         ┌──────────────────┐
                         │   Llama 3.2 LLM   │
                         │  (context-aware   │
                         │   answer generation)│
                         └────────┬──────────┘
                                  ▼
                         ┌──────────────────┐
                         │   Final Answer     │
                         │  (Streamlit UI)    │
                         └──────────────────┘
```

---

## 📦 Installation & Setup (Run Locally)

### Prerequisites
- Python 3.12
- [Ollama](https://ollama.com/download) installed

### 1. Clone the repository
```bash
git clone https://github.com/Shlokverma0/RAG-CHATBOT.git
cd RAG-CHATBOT
```

### 2. Set up a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Pull the required Ollama models
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 5. Add your documents
Place your `.pdf` or `.txt` files inside the `docs/` folder.

### 6. Build the vector database
```bash
python ingest.py
```
> ⚠️ Re-run this step any time you add or update documents in `docs/`.

### 7. Launch the chatbot

**Web UI:**
```bash
streamlit run app.py
```

**Terminal mode:**
```bash
python query.py
```

---

## 💡 Usage Examples

| Question                                  | Answer Source        |
|--------------------------------------------|-----------------------|
| "What is this project about?"              | Your documents (RAG)  |
| "Who is the current Prime Minister of India?" | Live web search     |
| "What is a large language model?"          | General knowledge      |

---

## 📁 Project Structure

```
RAG-CHATBOT/
├── app.py              # Streamlit web UI (local, Ollama-based)
├── ingest.py            # Document loader + vector DB builder (local)
├── query.py             # Core RAG + web search + LLM logic (local)
├── app_cloud.py          # Streamlit web UI (cloud deployment version)
├── ingest_cloud.py       # Vector DB builder for cloud deployment
├── query_cloud.py        # RAG + web search logic for cloud deployment
├── docs/                 # Your documents go here
├── chroma_db/            # Auto-generated vector database (gitignored)
├── requirements.txt      # Python dependencies
└── .gitignore
```

---

## 🚧 Future Improvements

- [ ] Support for `.docx` and `.csv` files
- [ ] GPU acceleration for faster inference
- [ ] Chat memory across sessions
- [ ] Multi-user support with authentication

---

## 👤 Author

**Shlok Verma**
B.Tech CSE Student | AI/ML Enthusiast

- GitHub: [@Shlokverma0](https://github.com/Shlokverma0)

---

## 📄 License

This project is licensed under the MIT License.
