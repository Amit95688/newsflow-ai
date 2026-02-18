from app.agents.summarize_stories import refresh_db_with_top_and_best
from app.database.fetch import get_top_story_summaries, get_best_story_summaries


def run_pipeline() -> None:
    print("Starting pipeline: scrape -> summarize -> database...")
    refresh_db_with_top_and_best()

    top_rows = get_top_story_summaries()
    best_rows = get_best_story_summaries()

    print("Pipeline completed successfully.")
    print(f"Top stories saved: {len(top_rows)}")
    print(f"Best stories saved: {len(best_rows)}")


if __name__ == "__main__":
    run_pipeline()