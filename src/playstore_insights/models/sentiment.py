"""Review sentiment classification with a TF-IDF + logistic regression pipeline."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

from ..config import RANDOM_STATE
from .export import export_text_classifier


@dataclass
class SentimentReport:
    vectorizer: TfidfVectorizer
    model: LogisticRegression
    metrics: dict
    top_terms: dict[str, list[dict]]

    def predict_proba(self, texts: list[str]) -> np.ndarray:
        return self.model.predict_proba(self.vectorizer.transform(texts))

    def export(self) -> dict:
        return export_text_classifier(self.vectorizer, self.model)

    def summary(self) -> dict:
        return {"metrics": self.metrics, "top_terms": self.top_terms}


def _top_terms(vectorizer: TfidfVectorizer, model: LogisticRegression, k: int) -> dict:
    vocab = np.array(vectorizer.get_feature_names_out())
    out = {}
    for label, weights in zip(model.classes_, model.coef_, strict=True):
        order = np.argsort(weights)[::-1][:k]
        out[str(label)] = [
            {"term": str(vocab[i]), "weight": round(float(weights[i]), 3)} for i in order
        ]
    return out


def train_sentiment_model(
    reviews: pd.DataFrame, max_features: int = 8000, top_k: int = 15
) -> SentimentReport:
    X_train, X_test, y_train, y_test = train_test_split(
        reviews["text"],
        reviews["sentiment"],
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=reviews["sentiment"],
    )
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), min_df=2, max_features=max_features, sublinear_tf=True
    )
    model = LogisticRegression(C=10, max_iter=2000)
    model.fit(vectorizer.fit_transform(X_train), y_train)
    pred = model.predict(vectorizer.transform(X_test))
    labels = model.classes_.tolist()
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "f1_macro": round(float(f1_score(y_test, pred, average="macro")), 4),
        "labels": labels,
        "confusion": confusion_matrix(y_test, pred, labels=labels).tolist(),
        "n_train": len(X_train),
        "n_test": len(X_test),
        "vocabulary_size": len(vectorizer.vocabulary_),
    }
    return SentimentReport(vectorizer, model, metrics, _top_terms(vectorizer, model, top_k))
