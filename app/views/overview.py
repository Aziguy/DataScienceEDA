import plotly.express as px
import streamlit as st

from components import data, hero
from playstore_insights import analytics

apps, reviews, quality = data()
k = analytics.kpis(apps, reviews)


def _n(value: int) -> str:
    return f"{value:,}".replace(",", "\u202f")


hero(
    "Google Play Store \u00b7 EDA & ML",
    "Le Play Store,",
    "d\u00e9cod\u00e9 par les donn\u00e9es.",
    f"{_n(k['apps'])} applications et {_n(k['labelled_reviews'])} avis nettoy\u00e9s, "
    "analys\u00e9s et mod\u00e9lis\u00e9s.",
)

cols = st.columns(5)
cols[0].metric("Applications", _n(k["apps"]))
cols[1].metric("Note moyenne", f"{k['avg_rating']:.2f}")
cols[2].metric("Gratuites", f"{k['free_share']:.1%}")
cols[3].metric("Installations", f"{k['total_installs'] / 1e9:.1f} Md")
cols[4].metric("Avis positifs", f"{k['positive_share']:.0%}")

stats = analytics.category_stats(apps)
left, right = st.columns([7, 5])
fig = px.bar(
    stats.head(15).sort_values("apps"),
    x="apps",
    y="category",
    orientation="h",
    title="Applications par catégorie",
    labels={"apps": "Applications", "category": ""},
)
left.plotly_chart(fig, width="stretch")

dist = analytics.rating_distribution(apps)
fig = px.bar(
    x=dist["bins"],
    y=dist["counts"],
    title="Distribution des notes",
    labels={"x": "Note", "y": "Applications"},
)
right.plotly_chart(fig, width="stretch")

tiers = analytics.installs_tiers(apps)
left, right = st.columns(2)
fig = px.bar(
    x=tiers["labels"],
    y=tiers["apps"],
    title="Applications par palier d'installations",
    labels={"x": "", "y": "Applications"},
)
left.plotly_chart(fig, width="stretch")
fig = px.line(
    x=tiers["labels"],
    y=tiers["avg_rating"],
    markers=True,
    title="Note moyenne par palier d'installations",
    labels={"x": "", "y": "Note moyenne"},
)
right.plotly_chart(fig, width="stretch")

with st.expander("Rapport de qualité des données"):
    st.json(quality.to_dict())
