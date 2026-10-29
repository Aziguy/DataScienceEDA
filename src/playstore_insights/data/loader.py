"""Raw CSV loading."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..config import PATHS


def load_apps(path: Path | str | None = None) -> pd.DataFrame:
    return pd.read_csv(
        path or PATHS.raw_apps, dtype=str, keep_default_na=False, na_values=["", "NaN"]
    )


def load_reviews(path: Path | str | None = None) -> pd.DataFrame:
    return pd.read_csv(path or PATHS.raw_reviews)
