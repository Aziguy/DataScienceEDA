"""App rating regression: candidate comparison, final model and portable export."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from ..config import RANDOM_STATE
from ..features import Feature, add_derived, build_spec, spec_to_dict, transform
from .export import export_gradient_boosting

LEGACY_COLUMNS = [0, 1, 2, 3]


def final_estimator() -> GradientBoostingRegressor:
    return GradientBoostingRegressor(
        n_estimators=400,
        learning_rate=0.03,
        max_depth=4,
        subsample=0.8,
        min_samples_leaf=20,
        random_state=RANDOM_STATE,
    )


def candidates() -> dict[str, object]:
    return {
        "Baseline (moyenne)": DummyRegressor(),
        "KNN v1 (4 variables)": make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=3)),
        "Ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
        "Random Forest": RandomForestRegressor(
            n_estimators=300, min_samples_leaf=5, n_jobs=-1, random_state=RANDOM_STATE
        ),
        "Gradient Boosting": final_estimator(),
    }


@dataclass
class RatingReport:
    model: GradientBoostingRegressor
    spec: list[Feature]
    comparison: list[dict]
    holdout: dict
    importance: list[dict]
    predictions: pd.DataFrame
    metadata: dict = field(default_factory=dict)

    def export(self) -> dict:
        return {
            "features": spec_to_dict(self.spec),
            "model": export_gradient_boosting(self.model),
            "metadata": self.metadata,
        }

    def summary(self) -> dict:
        return {
            "comparison": self.comparison,
            "holdout": self.holdout,
            "importance": self.importance,
            "metadata": self.metadata,
        }


def _scores(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    return {
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 4),
        "r2": round(float(r2_score(y_true, y_pred)), 4),
        "within_half_star": round(float(np.mean(np.abs(y_true - y_pred) <= 0.5)), 4),
    }


def compare_models(X: np.ndarray, y: np.ndarray, folds: int = 5) -> list[dict]:
    cv = KFold(folds, shuffle=True, random_state=RANDOM_STATE)
    scoring = {"mae": "neg_mean_absolute_error", "rmse": "neg_root_mean_squared_error", "r2": "r2"}
    rows = []
    for name, estimator in candidates().items():
        data = X[:, LEGACY_COLUMNS] if name.startswith("KNN v1") else X
        res = cross_validate(estimator, data, y, cv=cv, scoring=scoring)
        rows.append(
            {
                "model": name,
                "mae": round(float(-res["test_mae"].mean()), 4),
                "rmse": round(float(-res["test_rmse"].mean()), 4),
                "r2": round(float(res["test_r2"].mean()), 4),
                "r2_std": round(float(res["test_r2"].std()), 4),
            }
        )
    return sorted(rows, key=lambda r: r["mae"])


def grouped_importance(model: GradientBoostingRegressor, spec: list[Feature]) -> list[dict]:
    groups: dict[str, float] = {}
    for feat, value in zip(spec, model.feature_importances_, strict=True):
        key = feat.source if feat.kind == "onehot" else feat.name
        groups[key] = groups.get(key, 0.0) + float(value)
    return [
        {"feature": k, "importance": round(v, 4)}
        for k, v in sorted(groups.items(), key=lambda kv: -kv[1])
    ]


def train_rating_model(apps: pd.DataFrame, compare: bool = True) -> RatingReport:
    df = add_derived(apps.loc[apps["rating"].notna()])
    spec = build_spec(df)
    X, y = transform(df, spec), df["rating"].to_numpy()
    comparison = compare_models(X, y) if compare else []

    idx_train, idx_test = train_test_split(
        np.arange(len(df)), test_size=0.2, random_state=RANDOM_STATE
    )
    model = final_estimator().fit(X[idx_train], y[idx_train])
    pred = model.predict(X[idx_test])
    predictions = pd.DataFrame(
        {
            "app": df["app"].to_numpy()[idx_test],
            "category": df["category"].to_numpy()[idx_test],
            "actual": y[idx_test],
            "predicted": np.round(pred, 3),
        }
    )
    metadata = {
        "target": "rating",
        "n_train": len(idx_train),
        "n_test": len(idx_test),
        "n_features": len(spec),
        "categories": sorted(df["category"].unique().tolist()),
        "content_ratings": sorted(df["content_rating"].unique().tolist()),
        "rating_mean": round(float(y.mean()), 4),
    }
    return RatingReport(
        model=model,
        spec=spec,
        comparison=comparison,
        holdout=_scores(y[idx_test], pred),
        importance=grouped_importance(model, spec),
        predictions=predictions,
        metadata=metadata,
    )
