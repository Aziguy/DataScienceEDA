#Mes imports
import re
import sys
import time
import datetime
import os
import pandas as pd
import numpy as np
import codecs
import streamlit as st
import streamlit.components.v1 as components
from sklearn.neighbors import KNeighborsClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.compose import make_column_transformer
from sklearn.compose import make_column_selector
from sklearn.preprocessing import LabelEncoder, LabelBinarizer, OrdinalEncoder, OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
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

@st.cache(persist=True)
def merge_file(dataset1, dataset2):
	temp1 = pd.read_csv(os.path.join(dataset1))
	temp2 = pd.read_csv(os.path.join(dataset2))
	dfword = pd.merge(temp1,temp2,on='App',how='outer')
	#Drop rows with incomplete data
	dfword.dropna(how ='any', inplace = True)
	return dfword

def nettoyage_db(dataset):
	return db_clear

# Transformer mes variables catégorielles
@st.cache(persist=True)
def transform_var_model(my_db):
	df = pd.read_csv(os.path.join(my_db))
	X = df
	y = df["Rating"]
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
	var_cat = ["Category","Type", "Genres", "Content Rating", "Android Ver"]
	var_num = ["Rating", "Reviews", "Size", "Installs", "Price"]
	numerical_pipeline = make_pipeline(SimpleImputer(), StandardScaler())
	categorical_pipeline = make_pipeline(SimpleImputer(strategy = 'most_frequent'), OneHotEncoder())
	preprocessor = make_column_transformer((numerical_pipeline, var_num), (categorical_pipeline, var_cat))
	# model
	model = make_pipeline(preprocessor, SGDClassifier())
	model.fit(X_train, y_train)
	le_score = model.score(X_test, y_test)
	return le_score

# Créer mon model
def make_model(my_db, my_db_target):
	X = my_db
	y = my_db_target
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
	# Model
	model = KNeighborsClassifier(n_neighbors=3)
	model.fit(X_train, y_train)
	le_score = model.score(X_test, y_test)
	return le_score