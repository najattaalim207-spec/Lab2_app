import pandas as pd
from google_play_scraper import search, app as gp_app, reviews
from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


def search_apps(term):
    """Search Google Play for apps matching the term, return a DataFrame."""
    results = search(term, lang="en", country="us")

    data = []
    for r in results[:10]:  # limit to 10 to keep things fast
        try:
            details = gp_app(r["appId"], lang="en", country="us")
            free = details.get("free", True)
            genre = details.get("genre", "Unknown")
            installs_raw = details.get("installs", "0")
        except Exception:
            free = True
            genre = "Unknown"
            installs_raw = "0"

        installs_clean = int(str(installs_raw).replace("+", "").replace(",", "") or 0)

        data.append({
            "AppId": r["appId"],
            "App": r["title"],
            "Score": r.get("score", 0) or 0,
            "Installs": installs_clean,
            "Free": free,
            "Genre": genre
        })

    return pd.DataFrame(data)


def get_reviews(app_id, count=10):
    """Return a list of review texts for a given app."""
    try:
        result, _ = reviews(app_id, lang="en", country="us", count=count)
        return [r["content"] for r in result if r["content"]]
    except Exception:
        return []


def sentiment_score(text):
    """Compute sentiment label/score for a single text (truncated to 512 chars)."""
    result = classifier(text[:512])
    return result[0]


def compute_app_sentiment(app_id, count=10):
    """Compute average sentiment score (-1 to 1) for an app based on its reviews."""
    texts = get_reviews(app_id, count)
    if not texts:
        return None, []

    details = []
    scores = []
    for t in texts:
        res = sentiment_score(t)
        val = res["score"] if res["label"] == "POSITIVE" else -res["score"]
        scores.append(val)
        details.append({"review": t, "label": res["label"], "score": res["score"]})

    avg = sum(scores) / len(scores)
    return avg, details