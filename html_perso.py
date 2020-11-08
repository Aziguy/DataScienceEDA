# HTML render

def entete_de_page():
	my_header = """
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
	  <div class="jumbotron">
  		<h1 class="display-4">Google PlayStore</h1>
  		<p class="lead">Exploratory Data Analysis (EDA) & Machine learning</p>
  		<hr class="my-4">
  		<p>Cette application met en exergue l'analyse exploiratoire du dataset contenant l'ensemble des applications androids issue de l'apps store. Cette base contient 13 colonnes parmi lesquelles nous pouvons citer : catergory, rating, size, etc.</p>
  		<a class="btn btn-primary btn-lg" href="https://www.kaggle.com/lava18/google-play-store-apps" target="_blank" role="button">En savoir plus</a>
</div>	
	"""
	return my_header

def pied_de_page():
	my_footer = """
	<!-- CSS CDN -->
	  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	  <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" type="text/css" rel="stylesheet" media="screen,projection"/>
	  <link href="static/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
	   <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">
	 <footer class="page-footer grey darken-4">
	    <div class="container" id="aboutapp">
	      <div class="row">
	        <div class="col l6 s12">
	          <h5 class="white-text">About Streamlit EDA App</h5>
	          <p class="grey-text text-lighten-4">Using Streamlit,Pandas,Pandas Profile and SweetViz.</p>
	        </div>
	      
	   <div class="col l3 s12">
	          <h5 class="white-text">Connect With Me</h5>
	          <ul>
	            <a href="https://facebook.com/jcharistech" target="_blank" class="white-text">
	            <i class="fab fa-facebook fa-4x"></i>
	          </a>
	          <a href="https://gh.linkedin.com/in/jesiel-emmanuel-agbemabiase-6935b690" target="_blank" class="white-text">
	            <i class="fab fa-linkedin fa-4x"></i>
	          </a>
	          <a href="https://www.youtube.com/channel/UC2wMHF4HBkTMGLsvZAIWzRg" target="_blank" class="white-text">
	            <i class="fab fa-youtube-square fa-4x"></i>
	          </a>
	           <a href="https://github.com/Jcharis/" target="_blank" class="white-text">
	            <i class="fab fa-github-square fa-4x"></i>
	          </a>
	          </ul>
	        </div>
	      </div>
	    </div>
	    <div class="footer-copyright">
	      <div class="container">
	      Made by <a class="white-text text-lighten-3" href="https://jcharistech.wordpress.com">Jesse E.Agbe & JCharisTech</a><br/>
	      <a class="white-text text-lighten-3" href="https://jcharistech.wordpress.com">Jesus Saves @JCharisTech</a>
	      </div>
	    </div>
	  </footer>
	"""
	return my_footer

def myfunction(entier, carrac):
	return entier, carrac