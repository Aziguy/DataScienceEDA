import pandas as pd
import plotly.express as px
import streamlit as st

from components import SENTIMENT_COLORS, data, hero, sentiment_model
from playstore_insights import analytics

apps, reviews, _ = data()
bundle = sentiment_model()
hero(
    "NLP · Analyse de sentiment",
    "Ce que disent",
    "les utilisateurs.",
    "TF-IDF et régression logistique entraînés sur près de 30 000 avis.",
)

text = st.text_area(
    "Avis (en anglais)", "This app is great, very easy to use and the update fixed every crash."
)
if text.strip():
    proba = bundle["model"].predict_proba(bundle["vectorizer"].transform([text]))[0]
    classes = bundle["model"].classes_
    best = classes[proba.argmax()]
    st.subheader(f"Verdict : {best} ({proba.max():.0%})")
    fig = px.bar(
        x=proba,
        y=classes,
        orientation="h",
        color=classes,
        color_discrete_map=SENTIMENT_COLORS,
        range_x=[0, 1],
        labels={"x": "Probabilité", "y": ""},
    )
    fig.update_layout(showlegend=False, height=220)
    st.plotly_chart(fig, width="stretch")

shares = analytics.sentiment_by_category(apps, reviews)
frame = pd.DataFrame(shares["series"], index=shares["categories"]).reset_index(names="category")
long = frame.melt(id_vars="category", var_name="sentiment", value_name="share")
fig = px.bar(
    long,
    x="share",
    y="category",
    color="sentiment",
    orientation="h",
    color_discrete_map=SENTIMENT_COLORS,
    title="Répartition du sentiment par catégorie",
    labels={"share": "", "category": ""},
    height=820,
)
fig.update_layout(yaxis={"categoryorder": "array", "categoryarray": shares["categories"][::-1]})
st.plotly_chart(fig, width="stretch")
