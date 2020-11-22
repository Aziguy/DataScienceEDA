#Mes imports
import re
import sys
import time
import datetime
import os
import pandas as pd
import codecs
import streamlit as st
import streamlit.components.v1 as components
#Mes méthodes utiles
"""
Cette méthode permet d'afficher une page html dans streamlit
Elle prend en entré un fichier html. Par défaut, nous lui donnons une largeur et une hauteur
"""
def st_display_sweetviz(report_html, hauteur=1000):
	report_file = codecs.open(report_html,'r')
	page = report_file.read()
	components.html(page,height=hauteur,scrolling=True)

@st.cache(persist=True)
def lire_dataset(dataset):
	df = pd.read_csv(os.path.join(dataset))
	return df

def nettoyage_db(dataset):
	return db_clear