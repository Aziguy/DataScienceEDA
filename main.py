# My imports
import html_perso as hp
import html_alert as ha
import utils
import streamlit as st
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport 
from PIL import Image
import streamlit.components.v1 as components
import sweetviz as sv 

# Config my page
img = Image.open('favicon.ico')
MY_CONFIG = {'page_title': 'Data science', 'page_icon': img}
st.set_page_config(**MY_CONFIG)

def main():
	"""We're going to create a beautiful app with Streamlit"""
	menu = ["Accueil", "Pandas Profile", "Sweetviz", "Visualisation", "A propos"]
	selection = st.sidebar.selectbox("Fonctions", menu)

	if selection == "Pandas Profile":
		components.html(ha.alert_panda_prof(), height=190)
		my_data = st.file_uploader("Charger le fichier CSV",type=['csv'])
		if my_data is not None:
			df = pd.read_csv(my_data)
			st.dataframe(df.head(10))
			eda_profil = ProfileReport(df)
			st_profile_report(eda_profil)
	elif selection == "Sweetviz":
		components.html(ha.alert_sweetviz(), height=190)
		data_file = st.file_uploader("Charger le fichier CSV",type=['csv'])
		if data_file is not None:
			df = pd.read_csv(data_file)
			st.dataframe(df.head(10))
			if st.button("Générer le rapport"):
				report = sv.analyze(df)
				report.show_html()
				utils.st_display_sweetviz("SWEETVIZ_REPORT.html")

	elif selection == "Visualisation":
		st.subheader("The best visualization of year ^_^")
	elif selection == "A propos":
		#st.subheader("Team presentation")
		components.html(hp.pied_de_page(),height=800)
		#components.iframe('http://www.ingemedia.net/',height=1000, scrolling=True)
	else:
		components.html(hp.entete_de_page(), height=1800)

if __name__ == '__main__':
	main()