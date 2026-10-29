"""Playstore Insights, Streamlit edition: `streamlit run app/streamlit_app.py`."""

import streamlit as st

st.set_page_config(page_title="Playstore Insights", page_icon="\U0001f4ca", layout="wide")

from components import inject_css  # noqa: E402

inject_css()
pages = [
    st.Page("views/overview.py", title="Vue d'ensemble", icon=":material/dashboard:", default=True),
    st.Page("views/explore.py", title="Exploration", icon=":material/travel_explore:"),
    st.Page("views/sentiment.py", title="Sentiment", icon=":material/forum:"),
    st.Page("views/predict.py", title="Prédiction", icon=":material/insights:"),
    st.Page("views/profiling.py", title="Profiling CSV", icon=":material/table_view:"),
]
st.navigation(pages).run()
