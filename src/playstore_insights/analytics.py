"""Aggregations feeding the dashboard, the static site and the Streamlit app."""

from __future__ import annotations

import numpy as np
import pandas as pd

INSTALL_TIERS = [0, 1e3, 1e5, 1e6, 1e7, 1e8, np.inf]
INSTALL_LABELS = ["< 1k", "1k-100k", "100k-1M", "1M-10M", "10M-100M", "100M+"]
NUMERIC_COLUMNS = ["rating", "reviews", "size_mb", "installs", "price", "android_min"]


def kpis(apps: pd.DataFrame, reviews: pd.DataFrame | None = None) -> dict:
    out = {
        "apps": len(apps),
        "categories": int(apps["category"].nunique()),
        "avg_rating": round(float(apps["rating"].mean()), 2),
        "free_share": round(float((apps["type"] == "Free").mean()), 4),
        "total_installs": float(apps["installs"].sum()),
        "total_reviews": int(apps["reviews"].sum()),
        "median_size_mb": round(float(apps["size_mb"].median()), 1),
        "last_update": apps["last_updated"].max().strftime("%Y-%m-%d"),
    }
    if reviews is not None:
        out["labelled_reviews"] = len(reviews)
        out["positive_share"] = round(float((reviews["sentiment"] == "Positive").mean()), 4)
    return out


def category_stats(apps: pd.DataFrame) -> pd.DataFrame:
    grouped = apps.groupby("category")
    stats = pd.DataFrame(
        {
            "apps": grouped.size(),
            "avg_rating": grouped["rating"].mean().round(3),
            "median_installs": grouped["installs"].median(),
            "total_installs": grouped["installs"].sum(),
            "paid_share": grouped["type"].apply(lambda s: (s == "Paid").mean()).round(4),
            "avg_price_paid": grouped["price"].apply(lambda s: s[s > 0].mean()).round(2),
        }
    )
    return stats.sort_values("apps", ascending=False).reset_index()


def rating_distribution(apps: pd.DataFrame, step: float = 0.1) -> dict:
    ratings = apps["rating"].dropna()
    edges = np.round(np.arange(1, 5 + step, step), 2)
    counts, _ = np.histogram(ratings, bins=np.append(edges, 5 + step) - step / 2)
    return {"bins": edges.tolist(), "counts": counts.tolist()}


def installs_tiers(apps: pd.DataFrame) -> dict:
    tiers = pd.cut(apps["installs"], INSTALL_TIERS, labels=INSTALL_LABELS, right=False)
    frame = apps.assign(tier=tiers).groupby("tier", observed=False)
    return {
        "labels": INSTALL_LABELS,
        "apps": frame.size().tolist(),
        "avg_rating": [None if pd.isna(v) else round(v, 3) for v in frame["rating"].mean()],
    }


def free_vs_paid(apps: pd.DataFrame) -> list[dict]:
    rows = []
    for kind, group in apps.groupby("type"):
        rows.append(
            {
                "type": kind,
                "apps": len(group),
                "avg_rating": round(float(group["rating"].mean()), 3),
                "median_installs": float(group["installs"].median()),
                "median_reviews": float(group["reviews"].median()),
            }
        )
    return rows


def content_rating_breakdown(apps: pd.DataFrame) -> list[dict]:
    counts = apps["content_rating"].value_counts()
    return [{"label": k, "apps": int(v)} for k, v in counts.items()]


def updates_by_year(apps: pd.DataFrame) -> dict:
    years = apps["last_updated"].dt.year.value_counts().sort_index()
    return {"years": years.index.astype(int).tolist(), "apps": years.astype(int).tolist()}


def correlation(apps: pd.DataFrame) -> dict:
    frame = apps[NUMERIC_COLUMNS].copy()
    frame["reviews"] = np.log1p(frame["reviews"])
    frame["installs"] = np.log1p(frame["installs"])
    corr = frame.corr(method="spearman").round(3)
    return {"columns": NUMERIC_COLUMNS, "matrix": corr.to_numpy().tolist()}


def top_apps(apps: pd.DataFrame, by: str = "reviews", n: int = 15) -> list[dict]:
    cols = ["app", "category", "rating", "reviews", "installs", "type"]
    top = apps.nlargest(n, by)[cols]
    return top.replace({np.nan: None}).to_dict(orient="records")


def scatter_sample(apps: pd.DataFrame, n: int = 1500, seed: int = 7) -> list[list]:
    frame = apps.dropna(subset=["rating", "size_mb"])
    sample = frame.sample(min(n, len(frame)), random_state=seed)
    return [
        [round(float(r.size_mb), 2), float(r.rating), int(r.reviews), r.type, r.app]
        for r in sample.itertuples()
    ]


def sentiment_by_category(apps: pd.DataFrame, reviews: pd.DataFrame, min_reviews: int = 100):
    merged = reviews.merge(apps[["app", "category"]], on="app", how="inner")
    shares = pd.crosstab(merged["category"], merged["sentiment"], normalize="index")
    counts = merged["category"].value_counts()
    shares = shares.loc[counts[counts >= min_reviews].index]
    shares = shares.reindex(columns=["Positive", "Neutral", "Negative"], fill_value=0)
    shares = shares.sort_values("Positive", ascending=False).round(4)
    return {
        "categories": shares.index.tolist(),
        "series": {c: shares[c].tolist() for c in shares.columns},
        "reviews": [int(counts[c]) for c in shares.index],
    }


def polarity_vs_rating(apps: pd.DataFrame, reviews: pd.DataFrame, min_reviews: int = 20):
    per_app = reviews.groupby("app").agg(polarity=("polarity", "mean"), n=("polarity", "size"))
    merged = per_app[per_app["n"] >= min_reviews].join(apps.set_index("app")[["rating"]])
    merged = merged.dropna()
    corr = float(merged["polarity"].corr(merged["rating"], method="spearman"))
    points = [
        [round(float(p), 3), float(r), int(n), app]
        for app, p, n, r in merged[["polarity", "n", "rating"]].itertuples()
    ]
    return {"spearman": round(corr, 3), "points": points}
