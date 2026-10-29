import plotly.express as px
import streamlit as st

from components import data, hero
from playstore_insights import analytics

apps, _, _ = data()
hero("Exploration", "Explorer", "le catalogue.", "Filtres croisés sur les 9 659 applications.")

c1, c2, c3, c4 = st.columns([2, 2, 1, 2])
query = c1.text_input("Recherche", placeholder="Nom de l'application")
categories = c2.multiselect("Catégories", sorted(apps["category"].unique()))
kind = c3.radio("Modèle", ["Tous", "Free", "Paid"], horizontal=False)
min_rating = c4.slider("Note minimale", 1.0, 5.0, 1.0, 0.1)

view = apps
if query:
    view = view[view["app"].str.contains(query, case=False, regex=False)]
if categories:
    view = view[view["category"].isin(categories)]
if kind != "Tous":
    view = view[view["type"] == kind]
if min_rating > 1:
    view = view[view["rating"] >= min_rating]

m1, m2, m3 = st.columns(3)
m1.metric("Applications", len(view))
m2.metric("Note moyenne", f"{view['rating'].mean():.2f}" if len(view) else "-")
m3.metric("Installations médianes", f"{view['installs'].median():,.0f}" if len(view) else "-")

st.dataframe(
    view[["app", "category", "rating", "reviews", "installs", "size_mb", "price", "last_updated"]],
    width="stretch",
    hide_index=True,
    column_config={
        "rating": st.column_config.ProgressColumn("Note", min_value=1, max_value=5, format="%.1f"),
        "last_updated": st.column_config.DateColumn("Mise à jour"),
    },
)

left, right = st.columns([7, 5])
sample = view.dropna(subset=["rating", "size_mb"])
sample = sample.sample(min(len(sample), 3000), random_state=0)
fig = px.scatter(
    sample,
    x="size_mb",
    y="rating",
    color="type",
    log_x=True,
    hover_name="app",
    opacity=0.6,
    title="Taille (Mo) et note",
)
left.plotly_chart(fig, width="stretch")

corr = analytics.correlation(apps)
fig = px.imshow(
    corr["matrix"],
    x=corr["columns"],
    y=corr["columns"],
    color_continuous_scale=["#e66767", "#262b38", "#3987e5"],
    zmin=-1,
    zmax=1,
    text_auto=".2f",
    title="Corrélations de Spearman",
)
right.plotly_chart(fig, width="stretch")
