from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import (
	engine,
	TopStories,
	BestStories,
	SummariesTopStories,
	SummariesBestStories,
)


def _rows_to_dicts(rows) -> list[dict]:
	items: list[dict] = []
	for story, summary in rows:
		items.append(
			{
				"id": story.id,
				"title": story.title,
				"author": story.author,
				"score": story.score,
				"url": story.url,
				"summary": summary,
			}
		)
	return items


def get_top_story_summaries() -> list[dict]:
	with Session(engine) as session:
		rows = session.execute(
			select(TopStories, SummariesTopStories.summary)
			.outerjoin(SummariesTopStories, TopStories.id == SummariesTopStories.id)
			.order_by(TopStories.score.desc())
		).all()
	return _rows_to_dicts(rows)


def get_best_story_summaries() -> list[dict]:
	with Session(engine) as session:
		rows = session.execute(
			select(BestStories, SummariesBestStories.summary)
			.outerjoin(SummariesBestStories, BestStories.id == SummariesBestStories.id)
			.order_by(BestStories.score.desc())
		).all()
	return _rows_to_dicts(rows)
