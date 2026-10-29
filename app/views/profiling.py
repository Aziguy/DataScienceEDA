import pandas as pd
import plotly.express as px
import streamlit as st

from components import hero

hero(
    "Outil",
    "Profiler",
    "n'importe quel CSV.",
    "Types, valeurs manquantes, statistiques et distributions, calculés localement.",
)

uploaded = st.file_uploader("Fichier CSV", type=["csv"])
if uploaded is None:
    st.info("Chargez un fichier pour lancer le profilage.")
    st.stop()

df = pd.read_csv(uploaded)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Lignes", f"{len(df):,}")
c2.metric("Colonnes", df.shape[1])
c3.metric("Cellules manquantes", f"{df.isna().mean().mean():.1%}")
c4.metric("Doublons", int(df.duplicated().sum()))

st.dataframe(df.head(50), width="stretch")

summary = pd.DataFrame(
    {
        "type": df.dtypes.astype(str),
        "manquants": df.isna().sum(),
        "uniques": df.nunique(),
    }
)
st.subheader("Colonnes")
st.dataframe(summary, width="stretch")

numeric = df.select_dtypes("number")
if not numeric.empty:
    st.subheader("Statistiques descriptives")
    st.dataframe(numeric.describe().T, width="stretch")
    column = st.selectbox("Distribution", numeric.columns)
    st.plotly_chart(px.histogram(df, x=column, nbins=40), width="stretch")
    if numeric.shape[1] > 1:
        st.plotly_chart(
            px.imshow(numeric.corr().round(2), text_auto=True, zmin=-1, zmax=1),
            width="stretch",
        )
