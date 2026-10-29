import numpy as np
import pandas as pd

from playstore_insights.features import (
    MISSING_FILL,
    OneHotFeature,
    add_derived,
    build_spec,
    spec_to_dict,
    transform,
)


def _frame():
    return pd.DataFrame(
        {
            "reviews": [0, 99],
            "installs": [0.0, 1000.0],
            "size_mb": [np.nan, 10.0],
            "price": [0.0, 1.5],
            "android_min": [4.1, np.nan],
            "n_genres": [1, 2],
            "last_updated": pd.to_datetime(["2018-08-01", "2019-01-01"]),
            "category": ["Game", "Tools"],
            "content_rating": ["Everyone", "Teen"],
        }
    )


def test_add_derived():
    df = add_derived(_frame(), reference="2018-08-08")
    assert df["days_since_update"].tolist() == [7, 0]
    assert df["reviews_per_install"].tolist() == [0.0, 0.099]


def test_spec_and_transform():
    df = add_derived(_frame())
    spec = build_spec(df, min_count=1)
    onehots = [f for f in spec if isinstance(f, OneHotFeature)]
    assert {f.name for f in onehots} == {
        "category=Game",
        "category=Tools",
        "content_rating=Everyone",
        "content_rating=Teen",
    }
    X = transform(df, spec)
    names = [f.name for f in spec]
    assert X.shape == (2, len(spec))
    assert X[0, names.index("size_mb")] == MISSING_FILL
    assert X[1, names.index("log_reviews")] == np.log1p(99)
    assert X[1, names.index("category=Tools")] == 1.0
    assert spec_to_dict(spec)[0] == {
        "name": "log_reviews",
        "source": "reviews",
        "transform": "log1p",
        "kind": "numeric",
    }


def test_rare_levels_are_dropped():
    df = add_derived(_frame())
    assert not any(f.kind == "onehot" for f in build_spec(df, min_count=5))
