import numpy as np
import pytest

from playstore_insights.features import add_derived, transform
from playstore_insights.models import train_rating_model, train_sentiment_model
from playstore_insights.models.export import predict_gradient_boosting
from playstore_insights.models.rating import compare_models


@pytest.fixture(scope="module")
def rating(apps):
    return train_rating_model(apps, compare=False)


@pytest.fixture(scope="module")
def sentiment(reviews):
    return train_sentiment_model(reviews, max_features=3000)


def test_rating_beats_baseline(rating, apps):
    baseline_mae = np.mean(np.abs(apps["rating"].dropna() - apps["rating"].mean()))
    assert rating.holdout["mae"] < baseline_mae
    assert rating.holdout["r2"] > 0.1
    assert rating.importance[0]["importance"] >= rating.importance[-1]["importance"]
    assert abs(sum(i["importance"] for i in rating.importance) - 1) < 1e-3


def test_rating_export_matches_sklearn(rating, apps):
    df = add_derived(apps.dropna(subset=["rating"]).head(200))
    X = transform(df, rating.spec)
    payload = rating.export()
    expected = rating.model.predict(X)
    actual = [predict_gradient_boosting(payload["model"], row) for row in X.tolist()]
    np.testing.assert_allclose(actual, expected, atol=1e-9)
    assert payload["features"][0]["name"] == "log_reviews"


def test_compare_models_ranks_candidates(apps):
    df = add_derived(apps.dropna(subset=["rating"]).sample(600, random_state=0))
    from playstore_insights.features import build_spec

    X = transform(df, build_spec(df))
    rows = compare_models(X, df["rating"].to_numpy(), folds=2)
    assert {r["model"] for r in rows} >= {"Gradient Boosting", "Baseline (moyenne)"}
    assert rows == sorted(rows, key=lambda r: r["mae"])


def test_sentiment_quality(sentiment):
    assert sentiment.metrics["accuracy"] > 0.85
    assert sentiment.metrics["labels"] == ["Negative", "Neutral", "Positive"]
    assert len(sentiment.top_terms["Positive"]) == 15
    proba = sentiment.predict_proba(["I love this app, great", "terrible, crashes, worst"])
    labels = sentiment.model.classes_
    assert labels[proba[0].argmax()] == "Positive"
    assert labels[proba[1].argmax()] == "Negative"


def test_sentiment_export_shape(sentiment):
    payload = sentiment.export()
    n = len(payload["vocabulary"])
    assert n == len(payload["idf"]) == len(payload["coef"][0])
    assert payload["classes"] == ["Negative", "Neutral", "Positive"]
