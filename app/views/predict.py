import datetime as dt

import pandas as pd
import streamlit as st

from components import data, hero, rating_model
from playstore_insights.features import add_derived, transform

apps, _, _ = data()
bundle = rating_model()
hero(
    "Machine Learning · Régression",
    "Prédire la note",
    "d'une application.",
    "Gradient boosting entraîné sur 8 000 applications notées.",
)

left, right = st.columns([7, 5])
with left:
    c1, c2 = st.columns(2)
    category = c1.selectbox("Catégorie", sorted(apps["category"].unique()), index=None)
    content = c2.selectbox("Public", sorted(apps["content_rating"].unique()), index=0)
    installs = c1.select_slider(
        "Installations", options=sorted(apps["installs"].unique()), value=100_000
    )
    reviews = c2.number_input("Nombre d'avis", min_value=0, value=2000, step=100)
    size = c1.number_input("Taille (Mo)", min_value=0.0, value=15.0, step=0.5)
    price = c2.number_input("Prix (USD)", min_value=0.0, value=0.0, step=0.5)
    updated = c1.date_input("Dernière mise à jour", dt.date(2018, 7, 1))
    android = c2.number_input("Android minimum", min_value=1.0, max_value=9.0, value=4.1, step=0.1)
    genres = st.slider("Nombre de genres", 1, 2, 1)

record = pd.DataFrame(
    [
        {
            "category": category or "Family",
            "content_rating": content,
            "installs": float(installs),
            "reviews": reviews,
            "size_mb": size,
            "price": price,
            "last_updated": pd.Timestamp(updated),
            "android_min": android,
            "n_genres": genres,
        }
    ]
)
prediction = float(bundle["model"].predict(transform(add_derived(record), bundle["spec"]))[0])
category_avg = apps.loc[apps["category"] == (category or "Family"), "rating"].mean()

with right:
    st.metric(
        "Note prédite",
        f"{min(5, max(1, prediction)):.2f} / 5",
        delta=f"{prediction - category_avg:+.2f} vs catégorie",
    )
    st.progress((min(5, max(1, prediction)) - 1) / 4)
    st.caption(f"Moyenne de la catégorie : {category_avg:.2f}")
