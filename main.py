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
import dtale
#import sweetviz as sv

# Config my page
img = Image.open('favicon.ico')
MY_CONFIG = {'page_title': 'Data science', 'page_icon': img}
st.set_page_config(**MY_CONFIG)

def main():
	"""We're going to create a beautiful app with Streamlit"""
	menu = ["Accueil", "Pandas Profile", "D-Tale", "Visualisation", "Machine Learning", "A propos"]
	selection = st.sidebar.selectbox("Fonctions", menu)

	if selection == "Pandas Profile":
		components.html(ha.alert_panda_prof(), height=190)
		my_data = st.file_uploader("Charger le fichier CSV",type=['csv'])
		if my_data is not None:
			df = pd.read_csv(my_data)
			st.dataframe(df.head(10))
			eda_profil = ProfileReport(df, title='Pandas Profiling Report...', explorative=True)
			st_profile_report(eda_profil)
	elif selection == "D-Tale":
		components.html(ha.alert_dtale(), height=190)
		data_file = st.file_uploader("Charger le fichier CSV",type=['csv'])
		if data_file is not None:
			df = pd.read_csv(data_file)
			st.dataframe(df.head())
			d = dtale.show(df)
			d.open_browser()
			if st.button("Générer le rapport"):
				report = sv.analyze(df)
				report.show_html()
				utils.st_display_sweetviz("SWEETVIZ_REPORT.html")
				components.html(ha.alert_warning(),1000)

	elif selection == "Visualisation":
		st.subheader("The best visualization of year ^_^")

	elif selection == "Machine Learning":
		st.subheader("Apprentissage machine") 

	elif selection == "A propos":
		#st.subheader("Team presentation")
		components.html(hp.pied_de_page(),height=800)
		#components.iframe('http://www.ingemedia.net/',height=1000, scrolling=True)
	else:
		components.html(hp.entete_de_page(), height=1600)

if __name__ == '__main__':
	main()