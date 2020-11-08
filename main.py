# My imports
import html_perso as hp
import streamlit as st
import pandas as pd
import codecs
from PIL import Image
import streamlit.components.v1 as components

# Config my page
img = Image.open('favicon.ico')
MY_CONFIG = {'page_title': 'Data science', 'page_icon': img}
st.set_page_config(**MY_CONFIG)

def main():
	"""We're going to create a beautiful app with Streamlit"""
	menu = ["Accueil", "Pandas Profile", "Sweetviz", "Visualisation", "A propos"]
	selection = st.sidebar.selectbox("Fonctions", menu)

	if selection == "Pandas Profile":
		st.subheader("Automated EDA with Pandas Profile")
	elif selection == "Sweetviz":
		st.subheader("Automated EDA with Sweetviz")
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


