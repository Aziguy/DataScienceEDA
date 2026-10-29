"""Static site assembly for GitHub Pages: web sources + generated JSON data."""

from __future__ import annotations

import json
import os
import shutil
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

from .. import __version__, pipeline
from ..config import PATHS, Paths
from .badges import badge, coverage_color, score_color

ARTIFACT_FILES = [
    "dashboard.json",
    "metrics.json",
    "rating_model.json",
    "sentiment_model.json",
    "predictions.json",
]
APP_COLUMNS = [
    "app",
    "category",
    "rating",
    "reviews",
    "installs",
    "size_mb",
    "price",
    "content_rating",
    "last_updated",
    "android_min",
]


def apps_table(csv_path: Path) -> dict:
    df = pd.read_csv(csv_path, usecols=APP_COLUMNS)[APP_COLUMNS]
    df["last_updated"] = df["last_updated"].str[:10]
    df = df.astype(object).where(df.notna(), None)
    rows = [[None if isinstance(v, float) and np.isnan(v) else v for v in r] for r in df.values]
    return {"columns": APP_COLUMNS, "rows": rows}


def _ensure_artifacts(paths: Paths) -> None:
    missing = [f for f in [*ARTIFACT_FILES, "apps_clean.csv"] if not (paths.artifacts / f).exists()]
    if missing:
        pipeline.run(paths)


def build_site(paths: Paths = PATHS, coverage: float | None = None) -> Path:
    _ensure_artifacts(paths)
    out = paths.site
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(paths.web, out)
    data_dir = out / "data"
    data_dir.mkdir(exist_ok=True)

    for name in ARTIFACT_FILES:
        shutil.copy2(paths.artifacts / name, data_dir / name)
    pipeline.write_json(data_dir / "apps.json", apps_table(paths.artifacts / "apps_clean.csv"))
    pipeline.write_json(
        data_dir / "meta.json",
        {
            "version": __version__,
            "built_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "commit": os.environ.get("GITHUB_SHA", "local")[:7],
        },
    )

    metrics = json.loads((paths.artifacts / "metrics.json").read_text("utf-8"))
    mae = metrics["rating"]["holdout"]["mae"]
    accuracy = metrics["sentiment"]["metrics"]["accuracy"]
    badges = {
        "rating-mae.json": badge("rating MAE", f"{mae:.3f}", score_color(1 - mae)),
        "sentiment-accuracy.json": badge(
            "sentiment acc.", f"{accuracy:.1%}", score_color(accuracy)
        ),
    }
    if coverage is not None:
        badges["coverage.json"] = badge("coverage", f"{coverage:.0f}%", coverage_color(coverage))
    for name, payload in badges.items():
        pipeline.write_json(out / "badges" / name, payload)
    (out / ".nojekyll").touch()
    return out
