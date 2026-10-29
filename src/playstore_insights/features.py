"""Feature specification shared by the Python models and the browser runtime."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd

from .config import REFERENCE_DATE

NUMERIC_TRANSFORMS = {
    "log1p": np.log1p,
    "identity": lambda x: x,
}


@dataclass(frozen=True)
class NumericFeature:
    name: str
    source: str
    transform: str = "identity"
    kind: str = "numeric"


@dataclass(frozen=True)
class OneHotFeature:
    name: str
    source: str
    value: str
    kind: str = "onehot"


Feature = NumericFeature | OneHotFeature

BASE_NUMERIC = [
    NumericFeature("log_reviews", "reviews", "log1p"),
    NumericFeature("log_installs", "installs", "log1p"),
    NumericFeature("size_mb", "size_mb"),
    NumericFeature("price", "price"),
    NumericFeature("days_since_update", "days_since_update"),
    NumericFeature("android_min", "android_min"),
    NumericFeature("n_genres", "n_genres"),
    NumericFeature("reviews_per_install", "reviews_per_install"),
]
CATEGORICAL_SOURCES = ["category", "content_rating"]
MISSING_FILL = -1.0


def add_derived(df: pd.DataFrame, reference: str = REFERENCE_DATE) -> pd.DataFrame:
    """Columns computed from raw fields, mirrored by `web/assets/js/lib/features.js`."""
    out = df.copy()
    ref = pd.Timestamp(reference)
    out["days_since_update"] = (ref - pd.to_datetime(out["last_updated"])).dt.days.clip(lower=0)
    out["reviews_per_install"] = out["reviews"] / out["installs"].clip(lower=1)
    return out


def build_spec(df: pd.DataFrame, min_count: int = 20) -> list[Feature]:
    """Numeric features plus one-hot columns for categorical levels seen at least `min_count`."""
    spec: list[Feature] = list(BASE_NUMERIC)
    for source in CATEGORICAL_SOURCES:
        counts = df[source].value_counts()
        for value in sorted(counts[counts >= min_count].index):
            spec.append(OneHotFeature(f"{source}={value}", source, value))
    return spec


def transform(df: pd.DataFrame, spec: list[Feature]) -> np.ndarray:
    """Build the model matrix; missing numeric values become `MISSING_FILL`."""
    columns = []
    for feat in spec:
        if isinstance(feat, NumericFeature):
            values = NUMERIC_TRANSFORMS[feat.transform](df[feat.source].astype(float))
            columns.append(np.nan_to_num(values.to_numpy(), nan=MISSING_FILL))
        else:
            columns.append((df[feat.source] == feat.value).to_numpy(dtype=float))
    return np.column_stack(columns)


def spec_to_dict(spec: list[Feature]) -> list[dict]:
    return [asdict(f) for f in spec]
