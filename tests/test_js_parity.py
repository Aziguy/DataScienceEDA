"""The browser runtime must reproduce the Python models on the same inputs."""

import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest

from playstore_insights.config import REFERENCE_DATE
from playstore_insights.features import add_derived, transform
from playstore_insights.models import train_rating_model, train_sentiment_model

NODE = shutil.which("node")
SCRIPT = Path(__file__).parent / "js" / "parity.mjs"
pytestmark = pytest.mark.skipif(NODE is None, reason="node is not installed")

RECORD_FIELDS = [
    "category",
    "content_rating",
    "installs",
    "reviews",
    "size_mb",
    "price",
    "android_min",
    "n_genres",
]


def _records(df):
    out = []
    for row in df.itertuples():
        record = {f: getattr(row, f) for f in RECORD_FIELDS}
        record = {k: None if isinstance(v, float) and np.isnan(v) else v for k, v in record.items()}
        record["last_updated"] = row.last_updated.strftime("%Y-%m-%d")
        out.append(record)
    return out


def test_browser_runtime_matches_python(apps, reviews):
    rating = train_rating_model(apps, compare=False)
    sentiment = train_sentiment_model(reviews, max_features=3000)
    sample = apps.dropna(subset=["rating"]).sample(300, random_state=1)
    texts = [*reviews["text"].sample(300, random_state=1), "", "Ünïcödé café 2nd"]

    payload = {
        "rating": rating.export(),
        "sentiment": sentiment.export(),
        "records": _records(sample),
        "texts": texts,
        "reference_date": REFERENCE_DATE,
    }
    result = subprocess.run(
        [NODE, str(SCRIPT)], input=json.dumps(payload), capture_output=True, text=True, check=True
    )
    out = json.loads(result.stdout)

    expected_rating = rating.model.predict(transform(add_derived(sample), rating.spec))
    np.testing.assert_allclose(out["rating"], expected_rating, atol=1e-9)
    np.testing.assert_allclose(out["sentiment"], sentiment.predict_proba(texts), atol=2e-3)
