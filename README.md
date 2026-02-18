# H-GEN-AI

H-GEN-AI is a Hacker News summarization app that:
- fetches top and best stories,
- summarizes article URLs using a local Ollama model,
- stores stories + summaries in SQLite,
- serves a Flask dashboard.

## Pipeline Overview

Single-pass flow:

1. Scrape story metadata from Hacker News API
2. Summarize each story URL with LangChain + Ollama
3. Save results in SQLite tables
4. Read and show summaries in the dashboard

Use `pipeline.py` to run this full flow in one command.

## Project Structure

```text
Dockerfile
main.py
pipeline.py
requirements.txt
app/
	agents/summarize_stories.py
	database/database.py
	database/fetch.py
	scrap/scrap.py
	template/dashboard.html
```

## Prerequisites

- Python 3.11+
- Ollama running locally (`http://localhost:11434` by default)
- Model available in Ollama (default: `llama3.2:3b`)

Install/pull model example:

```bash
ollama pull llama3.2:3b
```

## Local Setup

1. Create and activate a virtual environment
2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Optional `.env` values:

```env
OLLAMA_BASE=http://localhost:11434
SUMMARY_MODEL=llama3.2:3b
SUMMARY_WORKERS=4
```

## Run the Full Pipeline (One Pass)

```bash
python pipeline.py
```

Expected output includes saved record counts for top and best stories.

## Run the Flask Dashboard

```bash
python main.py
```

Open: `http://127.0.0.1:5000`

## Docker

Build image:

```bash
docker build -t h-gen-ai .
```

Run container:

```bash
docker run --rm -p 5000:5000 h-gen-ai
```

Current container command runs:

1. `python pipeline.py`
2. `python main.py`

## Notes

- Database file is created automatically as `hn_stories.db`.
- Some stories may not have article URLs; those rows are still saved with fallback summary text.
- If Ollama is not running or model is unavailable, summaries may be marked as unavailable.
