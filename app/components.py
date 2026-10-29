"""Cached data access, chart template and UI helpers for the Streamlit app."""

from __future__ import annotations

import sys
from pathlib import Path

import joblib
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from playstore_insights.config import PATHS
from playstore_insights.models import train_rating_model, train_sentiment_model
from playstore_insights.pipeline import load_clean

SERIES = ["#3987e5", "#d95926", "#199e70", "#c98500"]
SENTIMENT_COLORS = {"Positive": SERIES[2], "Neutral": SERIES[0], "Negative": SERIES[1]}

pio.templates["psi"] = go.layout.Template(
    layout=go.Layout(
        colorway=SERIES,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, system-ui, sans-serif", "color": "#a7b0c6"},
        xaxis={"gridcolor": "#1c2334", "linecolor": "#2c3447", "zeroline": False},
        yaxis={"gridcolor": "#1c2334", "linecolor": "#2c3447", "zeroline": False},
        margin={"l": 8, "r": 8, "t": 40, "b": 8},
        hoverlabel={"bgcolor": "#0e1320", "bordercolor": "#2c3447"},
        legend={"orientation": "h", "y": 1.08, "x": 0},
    )
)
pio.templates.default = "plotly_dark+psi"

CSS = """
<style>
[data-testid="stMetric"] {
  background: rgba(14, 19, 32, .74);
  border: 1px solid rgba(148, 163, 184, .13);
  border-radius: 16px;
  padding: 16px 18px;
}
[data-testid="stMetricLabel"] p {
  font-family: "JetBrains Mono", monospace;
  font-size: 11px;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: #747d96;
}
.psi-eyebrow {
  color: #22d3ee;
  font: 500 12px/1 "JetBrains Mono", monospace;
  letter-spacing: .12em;
  text-transform: uppercase;
}
.psi-title {
  font-size: 2.6rem;
  font-weight: 600;
  letter-spacing: -.02em;
  line-height: 1.1;
  margin: .4rem 0 .6rem;
}
.psi-title span {
  background: linear-gradient(100deg, #22d3ee, #a78bfa);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def hero(eyebrow: str, title: str, highlight: str, lead: str) -> None:
    st.markdown(
        f'<div class="psi-eyebrow">{eyebrow}</div>'
        f'<div class="psi-title">{title} <span>{highlight}</span></div>',
        unsafe_allow_html=True,
    )
    st.caption(lead)


@st.cache_data(show_spinner="Nettoyage des données...")
def data():
    return load_clean(PATHS)


@st.cache_resource(show_spinner="Chargement du modèle de notation...")
def rating_model():
    path = PATHS.artifacts / "rating.joblib"
    if path.exists():
        return joblib.load(path)
    report = train_rating_model(data()[0], compare=False)
    return {"model": report.model, "spec": report.spec}


@st.cache_resource(show_spinner="Chargement du modèle de sentiment...")
def sentiment_model():
    path = PATHS.artifacts / "sentiment.joblib"
    if path.exists():
        return joblib.load(path)
    report = train_sentiment_model(data()[1])
    return {"vectorizer": report.vectorizer, "model": report.model}
