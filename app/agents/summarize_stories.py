from __future__ import annotations

import os
import concurrent.futures
from typing import Optional
import requests
from bs4 import BeautifulSoup
import re

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.database.database import (
    engine,
    TopStories,
    BestStories,
    SummariesTopStories,
    SummariesBestStories,
)
from app.scrap.scrap import get_top_stories, get_best_stories


# ==============================
# CONFIG
# ==============================

load_dotenv()

OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://localhost:11434")
SUMMARY_MODEL = os.getenv("SUMMARY_MODEL", "llama3.2:3b")
MAX_WORKERS = int(os.getenv("SUMMARY_WORKERS", 4))


# ==============================
# GLOBAL LLM (reuse instance)
# ==============================

llm = Ollama(
    base_url=OLLAMA_BASE,
    model=SUMMARY_MODEL,
    temperature=0.2,
)

prompt = PromptTemplate.from_template(
    "You are a concise technical summarizer.\n\n"
    "Context:\n{context}\n\n"
    "Provide:\n"
    "- 2-3 sentence summary\n"
    "- 3 bullet points\n"
)

chain = prompt | llm | StrOutputParser()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
)

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8",
}


# ==============================
# SUMMARIZATION
# ==============================

def summarize_text(text: str) -> str:
    if not text or len(text.strip()) < 40:
        return "Summary unavailable"

    try:
        chunks = splitter.split_text(text)

        # Limit context size (avoid huge prompts)
        context = "\n\n".join(chunks[:4])

        return chain.invoke({"context": context})
    except Exception:
        return "Summary unavailable"


def _extractive_fallback_summary(story: dict, page_text: str = "") -> str:
    title = (story.get("title") or "Untitled").strip()
    hn_text = (story.get("text") or "").strip()
    author = story.get("author") or "unknown"
    score = story.get("score") or 0
    url = story.get("url") or ""

    source_text = page_text.strip() or hn_text or title
    source_text = re.sub(r"\s+", " ", source_text).strip()

    sentence_parts = re.split(r"(?<=[.!?])\s+", source_text)
    sentence_parts = [s for s in sentence_parts if s]

    primary = sentence_parts[0] if sentence_parts else source_text
    secondary = sentence_parts[1] if len(sentence_parts) > 1 else ""

    max_len = 280
    primary = primary[:max_len]
    secondary = secondary[:max_len]

    bullet_source = sentence_parts[2:5] if len(sentence_parts) > 2 else []
    if not bullet_source:
        bullet_source = [source_text[i : i + 120].strip() for i in range(0, min(len(source_text), 360), 120)]
    bullet_source = [b for b in bullet_source if b]

    summary_lines = [
        f"{title} is a Hacker News story by {author} with score {score}.",
        primary,
    ]
    if secondary:
        summary_lines.append(secondary)

    bullet_lines = bullet_source[:3]
    if url:
        bullet_lines.append(f"Source URL: {url}")

    return "\n".join(summary_lines + ["", *[f"- {line}" for line in bullet_lines[:3]]])


def _extract_page_text(url: str) -> str:
    response = requests.get(url, headers=REQUEST_HEADERS, timeout=12)
    response.raise_for_status()

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()

    article = soup.find("article")
    if article:
        text = article.get_text(" ", strip=True)
        if len(text) >= 200:
            return text

    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    merged = "\n".join(p for p in paragraphs if p)
    if len(merged) >= 200:
        return merged

    body_text = soup.get_text(" ", strip=True)
    return body_text


def summarize_url(url: Optional[str]) -> str:
    if not url:
        return "Summary unavailable"

    try:
        page_text = _extract_page_text(url)
        return summarize_text(page_text)

    except Exception:
        return "Summary unavailable"


# ==============================
# PARALLEL PROCESSING
# ==============================

def process_story(story: dict) -> tuple[int, str, str]:
    sid = story["id"]
    url = story.get("url")
    title = story.get("title") or "Untitled"
    hn_text = story.get("text") or ""
    page_text = ""

    if url:
        try:
            page_text = _extract_page_text(url)
            summary = summarize_text(page_text)
        except Exception:
            summary = "Summary unavailable"

        if summary.startswith("Summary unavailable"):
            fallback_input = f"Headline: {title}\n\nHN Text: {hn_text}" if hn_text else title
            summary = summarize_text(fallback_input)
            if summary.startswith("Summary unavailable"):
                summary = _extractive_fallback_summary(story, page_text)
    else:
        fallback_input = f"Headline: {title}\n\nHN Text: {hn_text}" if hn_text else title
        summary = summarize_text(fallback_input)
        if summary.startswith("Summary unavailable"):
            summary = _extractive_fallback_summary(story)

    return sid, url or "", summary


# ==============================
# DB REFRESH
# ==============================

def refresh_db_with_top_and_best():

    top = get_top_stories(limit=5)
    best = get_best_stories(limit=5)

    with Session(engine) as session:

        # Clear old data
        session.query(TopStories).delete()
        session.query(BestStories).delete()
        session.query(SummariesTopStories).delete()
        session.query(SummariesBestStories).delete()
        session.commit()

        # Insert stories first (fast)
        for s in top:
            session.add(
                TopStories(
                    id=s["id"],
                    title=s.get("title"),
                    author=s.get("author"),
                    score=s.get("score"),
                    url=s.get("url"),
                )
            )

        for s in best:
            session.add(
                BestStories(
                    id=s["id"],
                    title=s.get("title"),
                    author=s.get("author"),
                    score=s.get("score"),
                    url=s.get("url"),
                )
            )

        session.commit()

        # Parallel summarization
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            # Top stories summaries
            futures_top = [executor.submit(process_story, s) for s in top]
            for future in concurrent.futures.as_completed(futures_top):
                sid, url, summary = future.result()
                session.merge(
                    SummariesTopStories(
                        id=sid,
                        url=url,
                        summary=summary,
                    )
                )

            # Best stories summaries
            futures_best = [executor.submit(process_story, s) for s in best]
            for future in concurrent.futures.as_completed(futures_best):
                sid, url, summary = future.result()
                session.merge(
                    SummariesBestStories(
                        id=sid,
                        url=url,
                        summary=summary,
                    )
                )

        session.commit()


# ==============================
# ENTRYPOINT
# ==============================

if __name__ == "__main__":
    refresh_db_with_top_and_best()
    print("✅ DB refreshed with parallel LLM summaries.")
