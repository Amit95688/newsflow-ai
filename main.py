from flask import Flask, render_template

from app.database.fetch import get_top_story_summaries, get_best_story_summaries


app = Flask(__name__, template_folder="app/template")


@app.route("/")
def dashboard():
	top_summaries = get_top_story_summaries()
	best_summaries = get_best_story_summaries()

	return render_template(
		"dashboard.html",
		title="Hacker News Story Summaries",
		top_summaries=top_summaries,
		best_summaries=best_summaries,
	)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
