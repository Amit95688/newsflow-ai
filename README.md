# 🚀 Newsflow-ai
> AI-powered Hacker News summarization pipeline  
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Production_Server-000000?style=for-the-badge&logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-Agentic_AI-00C853?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-Local_Inference-111111?style=for-the-badge)
![Llama3](https://img.shields.io/badge/Llama3-3B_Model-8E44AD?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Lightweight_DB-003B57?style=for-the-badge&logo=sqlite)
![RAG Ready](https://img.shields.io/badge/RAG-Ready-FF9800?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![CI/CD](https://img.shields.io/badge/CI/CD-Automated-2088FF?style=for-the-badge&logo=github-actions)

---

## 🧠 Tech Stack

- 🐳 Docker
- 🔥 Flask
- 🧠 Ollama (Llama 3)
- 🔗 LangChain
- 🗄 SQLite
- 🐍 Python 3.11+

---

## ✨ What It Does

H-GEN-AI automatically:

1. Fetches Top & Best stories from Hacker News
2. Extracts article URLs
3. Summarizes articles using a local LLM (Llama3 via Ollama)
4. Stores metadata + summaries in SQLite
5. Serves a clean Flask dashboard

All in one pipeline run.

---

## 🏗 Architecture

HN API → Scraper → LangChain Agent → Ollama (Llama3)  
→ Summary Generation → SQLite Storage → Flask Dashboard

Single-pass execution via:

```bash
python pipeline.py
```

---

## 📂 Project Structure

```
Dockerfile
main.py
pipeline.py
requirements.txt

app/
 ├── agents/
 │    └── summarize_stories.py
 ├── database/
 │    ├── database.py
 │    └── fetch.py
 ├── scrap/
 │    └── scrap.py
 └── template/
      └── dashboard.html
```

---

## ⚙️ Prerequisites

- Python 3.11+
- Ollama running locally (`http://localhost:11434`)
- Model available (default: `llama3.2:3b`)

Pull model:

```bash
ollama pull llama3.2:3b
```

---

## 🔧 Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run full pipeline:

```bash
python pipeline.py
```

Run dashboard:

```bash
python main.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 🐳 Docker

Build image:

```bash
docker build -t h-gen-ai .
```

Run container:

```bash
docker run --rm -p 5000:5000 h-gen-ai
```

Container automatically:
1. Runs pipeline
2. Starts Flask server

---

## 🌎 Environment Variables (Optional)

Create `.env`:

```env
OLLAMA_BASE=http://localhost:11434
SUMMARY_MODEL=llama3.2:3b
SUMMARY_WORKERS=4
```

---

## 🗄 Database

- SQLite auto-creates: `hn_stories.db`
- Stores:
  - story id
  - title
  - url
  - score
  - summary
  - category (top/best)

---

## ⚡ Why This Project Is Impressive

- Fully local LLM stack (no OpenAI dependency)
- Clean modular architecture
- Containerized production-ready setup
- Parallel summarization workers
- Extendable to RAG systems
- Real-world scraping + AI pipeline

---

## 🔥 Future Upgrades

- Vector search (Chroma / FAISS)
- Semantic filtering
- Topic clustering
- Email digest generator
- Auth system
- Background job queue
- CI/CD pipeline

---

## 📌 License

MIT

---
