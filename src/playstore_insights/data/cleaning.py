"""Typed, reproducible cleaning of the raw Play Store exports."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

import numpy as np
import pandas as pd

COLUMNS = {
    "App": "app",
    "Category": "category",
    "Rating": "rating",
    "Reviews": "reviews",
    "Size": "size_mb",
    "Installs": "installs",
    "Type": "type",
    "Price": "price",
    "Content Rating": "content_rating",
    "Genres": "genres",
    "Last Updated": "last_updated",
    "Current Ver": "current_ver",
    "Android Ver": "android_ver",
}

_SIZE_RE = re.compile(r"^\s*([\d.]+)\s*([kKmMgG])\s*$")
_ANDROID_RE = re.compile(r"^\s*(\d+)(?:\.(\d+))?")
_UNITS_MB = {"k": 1 / 1024, "m": 1.0, "g": 1024.0}


@dataclass
class QualityReport:
    raw_rows: int = 0
    malformed_rows: int = 0
    exact_duplicates: int = 0
    app_duplicates: int = 0
    clean_rows: int = 0
    missing: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def parse_size(value: object) -> float:
    """'19M' -> 19.0, '201k' -> 0.196, 'Varies with device' -> NaN."""
    if not isinstance(value, str):
        return np.nan
    match = _SIZE_RE.match(value)
    if not match:
        return np.nan
    number, unit = match.groups()
    return round(float(number) * _UNITS_MB[unit.lower()], 4)


def parse_installs(value: object) -> float:
    """'1,000,000+' -> 1_000_000."""
    if not isinstance(value, str):
        return np.nan
    digits = value.replace(",", "").replace("+", "").strip()
    return float(digits) if digits.isdigit() else np.nan


def parse_price(value: object) -> float:
    """'$4.99' -> 4.99, '0' -> 0.0."""
    if not isinstance(value, str):
        return np.nan
    try:
        return float(value.replace("$", "").strip())
    except ValueError:
        return np.nan


def parse_android(value: object) -> float:
    """'4.0.3 and up' -> 4.0, '5.0 - 8.0' -> 5.0, 'Varies with device' -> NaN."""
    if not isinstance(value, str):
        return np.nan
    match = _ANDROID_RE.match(value)
    if not match:
        return np.nan
    major, minor = match.groups()
    return float(f"{major}.{minor or 0}")


def _is_malformed(df: pd.DataFrame) -> pd.Series:
    rating = pd.to_numeric(df["rating"], errors="coerce")
    bad_rating = rating.notna() & ~rating.between(1, 5)
    bad_reviews = ~df["reviews"].astype(str).str.fullmatch(r"\d+")
    return bad_rating | bad_reviews


def clean_apps(raw: pd.DataFrame) -> tuple[pd.DataFrame, QualityReport]:
    """Return a typed, deduplicated apps table and its quality report."""
    report = QualityReport(raw_rows=len(raw))
    df = raw.rename(columns=COLUMNS)[list(COLUMNS.values())].copy()

    malformed = _is_malformed(df)
    report.malformed_rows = int(malformed.sum())
    df = df.loc[~malformed]

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["reviews"] = df["reviews"].astype(int)
    df["size_mb"] = df["size_mb"].map(parse_size)
    df["installs"] = df["installs"].map(parse_installs)
    df["price"] = df["price"].map(parse_price)
    df["android_min"] = df["android_ver"].map(parse_android)
    df["last_updated"] = pd.to_datetime(df["last_updated"], format="%B %d, %Y", errors="coerce")
    df["type"] = np.where(df["price"].fillna(0) > 0, "Paid", "Free")
    df["genres"] = df["genres"].fillna("")
    df["primary_genre"] = df["genres"].str.split(";").str[0]
    df["n_genres"] = df["genres"].str.count(";") + 1
    df["category"] = df["category"].str.replace("_", " ").str.title().str.replace(" And ", " & ")

    report.exact_duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates()
    before = len(df)
    df = (
        df.sort_values(["reviews", "last_updated"], ascending=False)
        .drop_duplicates(subset="app", keep="first")
        .sort_index()
        .reset_index(drop=True)
    )
    report.app_duplicates = before - len(df)
    report.clean_rows = len(df)
    report.missing = {k: int(v) for k, v in df.isna().sum().items() if v}
    return df, report


def clean_reviews(raw: pd.DataFrame) -> pd.DataFrame:
    """Keep labelled reviews with non-empty text."""
    df = raw.rename(
        columns={
            "App": "app",
            "Translated_Review": "text",
            "Sentiment": "sentiment",
            "Sentiment_Polarity": "polarity",
            "Sentiment_Subjectivity": "subjectivity",
        }
    )
    df = df.dropna(subset=["text", "sentiment"])
    df = df.loc[df["text"].str.strip().str.len() > 0]
    return df.drop_duplicates().reset_index(drop=True)
