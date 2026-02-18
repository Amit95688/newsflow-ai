# 🚀 H-GEN-AI

> AI-powered Hacker News summarization pipeline  
> Fully local • Dockerized • LLM-driven • Clean architecture

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

Built with 💻 + 🧠 AI
