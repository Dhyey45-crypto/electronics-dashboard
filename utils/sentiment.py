"""
Sentiment analysis helpers powered by TextBlob.
Used to auto-label customer reviews as Positive / Neutral / Negative
and to compute an aggregate sentiment score per product.
"""
from textblob import TextBlob


def analyze_review(text: str):
    """Return (label, emoji, polarity) for a single review string."""
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.15:
        return "Positive", "🟢", polarity
    elif polarity < -0.15:
        return "Negative", "🔴", polarity
    return "Neutral", "🟡", polarity


def analyze_reviews(reviews: list[str]):
    """Return a list of dicts with text, label, emoji, polarity for each review."""
    results = []
    for r in reviews:
        label, emoji, polarity = analyze_review(r)
        results.append({"text": r, "label": label, "emoji": emoji, "polarity": polarity})
    return results


def aggregate_sentiment(reviews: list[str]) -> float:
    """Average polarity across all reviews for a product, range -1..1."""
    if not reviews:
        return 0.0
    scores = [TextBlob(r).sentiment.polarity for r in reviews]
    return sum(scores) / len(scores)
