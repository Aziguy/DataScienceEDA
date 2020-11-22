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
import plotly.express as px
import plotly.figure_factory as ff
from sklearn import metrics
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
#import sweetviz as sv

# Config my page
img = Image.open('favicon.ico')
MY_CONFIG = {'page_title': 'Data science', 'page_icon': img}
st.set_page_config(**MY_CONFIG)
my_db = "datas/googleplaystore.csv"
my_db_clean = "datas/GooglePlayStore_Cleaned.csv"
my_reviews = "datas/googleplaystore_user_reviews.csv"

def main():
	"""We're going to create a beautiful app with Streamlit"""
	menu = ["Accueil", "Pandas Profile", "D-Tale", "Visualisation", "Nuage de mots", "Machine Learning", "A propos"]
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
		# Image d'entête
		image = Image.open('dataviz.png')
		col2,col1 = st.beta_columns([1,3])
		col2.image("https://idoc-projets.ias.u-psud.fr/redmine/attachments/download/121/sunburst.gif", caption='', width=None, use_column_width=True)
		col1.image(image, caption='', width=None, use_column_width=True)
		# Visualisation catégorie / rating / reviews
		cat1,cat2 = st.beta_columns(2)
		datas = utils.lire_dataset(my_db_clean)
		fig = px.histogram(datas,x='Rating',y='Category',title='Somme des notes par catégorie',color='Category')
		cat1.plotly_chart(fig)
		fig = px.histogram(datas,x='Reviews',y='Category',title='Somme des commentaires par catégorie',color='Category')
		cat2.plotly_chart(fig)
		# Visualisation sunburst / pie
		perc1,perc2 = st.beta_columns(2)
		fig = px.sunburst(datas, path=['Type','Category','Genres'], title='Types, Catégories et genres')
		perc1.plotly_chart(fig)
		fig = px.pie(datas, names='Type', title='Pourcentage apllication gratuites/Payantes',color_discrete_sequence=px.colors.sequential.RdBu)
		perc2.plotly_chart(fig)
		# Visualisation histo
		hist1,hist2 = st.beta_columns(2)
		hist_data = [list(datas['Rating'])]
		group_labels = ['Rating']
		fig = ff.create_distplot(hist_data, group_labels)
		hist1.plotly_chart(fig)
	elif selection == "Nuage de mots":
		img1,img2 = st.beta_columns(2)
		img1.image('datas/wordcloud/general.png')
		img2.image('datas/wordcloud/free_app.png')
		img3,img4 = st.beta_columns(2)
		img3.image('datas/wordcloud/free_app_pos.png')
		img4.image('datas/wordcloud/free_app_neg.png')
		img5,img6 = st.beta_columns(2)
		img5.image('datas/wordcloud/paid_app.png')
		img6.image('datas/wordcloud/paid_app_pos.png')
		img7,img8 = st.beta_columns(2)
		img7.image('datas/wordcloud/paid_app_neg.png')
	elif selection == "Machine Learning":
		image = Image.open('machine learning.jpg')
		col1,col2 = st.beta_columns([3,1])
		col2.image("https://static.wixstatic.com/media/bb7b70_d5fde322f7914060b7d997ba9d506a50~mv2.gif", caption='', width=None, use_column_width=True)
		col1.image(image, caption='', width=None, use_column_width=True)
		if st.checkbox("Afficher le dataset"):
			datas = utils.lire_dataset(my_db)
			st.write(datas.head())
		if st.checkbox("Afficher graph valeurs manquantes"):
			col1,col2 = st.beta_columns([2,1])
			df = datas.isnull()
			fig = px.imshow(df)
			col1.plotly_chart(fig)
			col2.write(datas.isnull().sum())
			col2.write("On peut voir que la colonne **Rating** contient la plupart des valeurs manquantes. A sa suite on a **Current Ver**, **Adroid ver** et **Type**.")
		if st.checkbox("Afficher DB ok"):
			datas = utils.lire_dataset(my_db_clean)
			st.write(datas.head())
			fig = px.scatter_matrix(datas, dimensions=["Rating", "Reviews", "Size", "Installs", "Price"], color="Type", symbol="Type", title="Matrix de dispersion des variables continues")
			fig.update_traces(diagonal_visible=False)
			st.plotly_chart(fig)
	elif selection == "A propos":
		#st.subheader("Team presentation")
		components.html(hp.pied_de_page(),height=800)
		#components.iframe('http://www.ingemedia.net/',height=1000, scrolling=True)
	else:
		components.html(hp.entete_de_page(), height=1600)

if __name__ == '__main__':
	main()