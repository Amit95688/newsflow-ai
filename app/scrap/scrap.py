import requests
from bs4 import BeautifulSoup

BASE_URL = "https://hacker-news.firebaseio.com/v0"


def fetch_story(story_id: int) -> dict:
    response = requests.get(f"{BASE_URL}/item/{story_id}.json", timeout=5)
    response.raise_for_status()
    story = response.json()

    raw_text = story.get("text") or ""
    clean_text = ""
    if raw_text:
        clean_text = BeautifulSoup(raw_text, "html.parser").get_text(" ", strip=True)

    return {
        "id": story_id,
        "title": story.get("title") or "Untitled",
        "author": story.get("by") or "unknown",
        "score": story.get("score") or 0,
        "url": story.get("url") or "",
        "text": clean_text,
    }


def get_top_stories(limit: int = 5) -> list[dict]:
    response = requests.get(f"{BASE_URL}/topstories.json", timeout=5)
    response.raise_for_status()
    story_ids = response.json()

    stories = []
    for story_id in story_ids[:limit]:
        stories.append(fetch_story(story_id))

    return stories


def get_best_stories(limit: int = 5) -> list[dict]:
    response = requests.get(f"{BASE_URL}/beststories.json", timeout=5)
    response.raise_for_status()
    story_ids = response.json()

    stories = []
    for story_id in story_ids[:limit]:
        stories.append(fetch_story(story_id))

    return stories


if __name__ == "__main__":
    print("Top Stories:")
    for story in get_top_stories():
        print(story)

    print("\nBest Stories:")
    for story in get_best_stories():
        print(story)
