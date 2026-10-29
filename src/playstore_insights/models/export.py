"""Portable JSON exports of fitted models, evaluated identically in Python and JavaScript."""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def export_gradient_boosting(model: GradientBoostingRegressor) -> dict:
    """Flatten every tree as parallel arrays; leaves have feature == -1."""
    trees = []
    for estimator in model.estimators_[:, 0]:
        tree = estimator.tree_
        leaf = tree.children_left == -1
        trees.append(
            {
                "f": np.where(leaf, -1, tree.feature).tolist(),
                "t": np.where(leaf, 0.0, tree.threshold).tolist(),
                "l": tree.children_left.tolist(),
                "r": tree.children_right.tolist(),
                "v": tree.value[:, 0, 0].tolist(),
            }
        )
    return {
        "type": "gradient_boosting",
        "init": float(model.init_.constant_[0][0]),
        "learning_rate": float(model.learning_rate),
        "trees": trees,
    }


def _float32(x: float) -> float:
    return float(np.float32(x))


def predict_gradient_boosting(payload: dict, row: list[float]) -> float:
    """Reference evaluator mirrored by `web/assets/js/lib/models.js`."""
    x = [_float32(v) for v in row]
    total = 0.0
    for tree in payload["trees"]:
        node = 0
        while tree["f"][node] != -1:
            node = tree["l"][node] if x[tree["f"][node]] <= tree["t"][node] else tree["r"][node]
        total += tree["v"][node]
    return payload["init"] + payload["learning_rate"] * total


def export_text_classifier(
    vectorizer: TfidfVectorizer, model: LogisticRegression, decimals: int = 5
) -> dict:
    vocab = sorted(vectorizer.vocabulary_, key=vectorizer.vocabulary_.get)
    return {
        "type": "tfidf_logreg",
        "ngram_range": list(vectorizer.ngram_range),
        "sublinear_tf": bool(vectorizer.sublinear_tf),
        "vocabulary": vocab,
        "idf": np.round(vectorizer.idf_, decimals).tolist(),
        "classes": model.classes_.tolist(),
        "coef": np.round(model.coef_, decimals).tolist(),
        "intercept": np.round(model.intercept_, decimals).tolist(),
    }
