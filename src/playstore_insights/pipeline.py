"""End-to-end pipeline: clean, analyse, train and persist artifacts."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import joblib
import pandas as pd

from . import analytics
from .config import PATHS, Paths
from .data import QualityReport, clean_apps, clean_reviews, load_apps, load_reviews
from .models import RatingReport, SentimentReport, train_rating_model, train_sentiment_model

log = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    apps: pd.DataFrame
    reviews: pd.DataFrame
    quality: QualityReport
    rating: RatingReport
    sentiment: SentimentReport


def load_clean(paths: Paths = PATHS) -> tuple[pd.DataFrame, pd.DataFrame, QualityReport]:
    apps, quality = clean_apps(load_apps(paths.raw_apps))
    return apps, clean_reviews(load_reviews(paths.raw_reviews)), quality


def write_json(path: Path, payload: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), "utf-8")
    return path


def dashboard_payload(result: PipelineResult) -> dict:
    apps, reviews = result.apps, result.reviews
    return {
        "kpis": analytics.kpis(apps, reviews),
        "quality": result.quality.to_dict(),
        "categories": analytics.category_stats(apps)
        .replace({float("nan"): None})
        .to_dict(orient="records"),
        "rating_distribution": analytics.rating_distribution(apps),
        "installs_tiers": analytics.installs_tiers(apps),
        "free_vs_paid": analytics.free_vs_paid(apps),
        "content_rating": analytics.content_rating_breakdown(apps),
        "updates_by_year": analytics.updates_by_year(apps),
        "correlation": analytics.correlation(apps),
        "top_reviews": analytics.top_apps(apps, "reviews"),
        "scatter": analytics.scatter_sample(apps),
        "sentiment_by_category": analytics.sentiment_by_category(apps, reviews),
        "polarity_vs_rating": analytics.polarity_vs_rating(apps, reviews),
    }


def run(paths: Paths = PATHS, compare: bool = True) -> PipelineResult:
    apps, reviews, quality = load_clean(paths)
    log.info("Cleaned %d apps and %d reviews", len(apps), len(reviews))
    rating = train_rating_model(apps, compare=compare)
    log.info("Rating model holdout: %s", rating.holdout)
    sentiment = train_sentiment_model(reviews)
    log.info("Sentiment model: accuracy=%s", sentiment.metrics["accuracy"])
    result = PipelineResult(apps, reviews, quality, rating, sentiment)
    save_artifacts(result, paths.artifacts)
    return result


def save_artifacts(result: PipelineResult, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    result.apps.to_csv(out / "apps_clean.csv", index=False)
    joblib.dump({"model": result.rating.model, "spec": result.rating.spec}, out / "rating.joblib")
    joblib.dump(
        {"vectorizer": result.sentiment.vectorizer, "model": result.sentiment.model},
        out / "sentiment.joblib",
    )
    write_json(out / "rating_model.json", result.rating.export())
    write_json(out / "sentiment_model.json", result.sentiment.export())
    write_json(
        out / "metrics.json",
        {"rating": result.rating.summary(), "sentiment": result.sentiment.summary()},
    )
    write_json(out / "dashboard.json", dashboard_payload(result))
    sample = result.rating.predictions.sample(
        min(800, len(result.rating.predictions)), random_state=0
    )
    write_json(out / "predictions.json", sample.to_dict(orient="split")["data"])
