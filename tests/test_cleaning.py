import math

import pandas as pd
import pytest

from playstore_insights.data import clean_apps, clean_reviews
from playstore_insights.data.cleaning import (
    parse_android,
    parse_installs,
    parse_price,
    parse_size,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("19M", 19.0), ("1.5G", 1536.0), ("512k", 0.5), ("Varies with device", None), (None, None)],
)
def test_parse_size(raw, expected):
    result = parse_size(raw)
    assert math.isnan(result) if expected is None else result == pytest.approx(expected)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("1,000,000+", 1e6), ("0", 0.0), ("Free", None), (3, None)],
)
def test_parse_installs(raw, expected):
    result = parse_installs(raw)
    assert math.isnan(result) if expected is None else result == expected


@pytest.mark.parametrize(("raw", "expected"), [("$4.99", 4.99), ("0", 0.0), ("Everyone", None)])
def test_parse_price(raw, expected):
    result = parse_price(raw)
    assert math.isnan(result) if expected is None else result == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("4.0.3 and up", 4.0),
        ("5.0 - 8.0", 5.0),
        ("4.4W and up", 4.4),
        ("7 and up", 7.0),
        ("Varies with device", None),
        (None, None),
    ],
)
def test_parse_android(raw, expected):
    result = parse_android(raw)
    assert math.isnan(result) if expected is None else result == expected


def test_clean_apps_on_fixture(tiny_raw):
    df, report = clean_apps(tiny_raw)
    assert report.raw_rows == 6
    assert report.malformed_rows == 1
    assert report.exact_duplicates == 1
    assert report.app_duplicates == 1
    assert list(df["app"]) == ["Alpha", "Beta", "Gamma"]
    alpha = df.set_index("app").loc["Alpha"]
    assert alpha["reviews"] == 300
    assert alpha["category"] == "Art & Design"
    beta = df.set_index("app").loc["Beta"]
    assert beta["type"] == "Paid" and beta["price"] == 2.99 and beta["n_genres"] == 2
    assert pd.isna(beta["size_mb"]) and pd.isna(beta["android_min"])
    assert report.missing["rating"] == 1


def test_clean_apps_full_dataset(apps):
    assert len(apps) > 9000
    assert apps["app"].is_unique
    assert apps["rating"].dropna().between(1, 5).all()
    assert (apps["installs"] >= 0).all()
    assert apps["last_updated"].notna().all()
    assert set(apps["type"]) == {"Free", "Paid"}


def test_clean_reviews_drops_empty():
    raw = pd.DataFrame(
        {
            "App": ["a", "a", "b", "c"],
            "Translated_Review": ["good", "good", None, "  "],
            "Sentiment": ["Positive", "Positive", None, "Neutral"],
            "Sentiment_Polarity": [0.7, 0.7, None, 0.0],
            "Sentiment_Subjectivity": [0.6, 0.6, None, 0.0],
        }
    )
    df = clean_reviews(raw)
    assert len(df) == 1 and df.loc[0, "sentiment"] == "Positive"
