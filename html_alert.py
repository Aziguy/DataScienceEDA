# HTML render

def alert_panda_prof():
	my_alert = """
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
	  <!-- Code alert panda_prof -->
	  <div class="alert alert-primary" role="alert">
  		<h4 class="alert-heading">EDA avec Pandas Profile</h4>
  		<p>Avec cette librairie, il est possible d'analyser automatiquement ses données (il est assez complet et à la portée de tous). Simple et rapide à mettre en œuvre, il est difficile de passer à coté de ce petit bijoux du profiling.</p>
  		<hr>
  		<p class="mb-0">Il suffit juste de charger un csv, et d'observer les résultats <i class="glyphicon glyphicon-stats" aria-hidden="true"></i>. Attention, selon le nombre de lignes et de colonnes de votre Dataset, le temps de traitement peut d'être très long! <i class="glyphicon glyphicon-time" aria-hidden="true"></i></p>
	  </div>
	"""
	return my_alert

def alert_dtale():
	my_alert = """
	<!-- SCRIPT CDN -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
	  <!-- Code alert D-Tale -->
	  <div class="alert alert-primary" role="alert">
  		<h4 class="alert-heading">EDA avec D-Tale</h4>
  		<p>D-Tale est une combinaison de Flask (côté back-end Flask) et React (côté front-end). C'est un moyen assez facile pour la visualisation et l'analyse des structures de données tels que les DataFrame.</p>
  		<hr>
  		<p class="mb-0">Il suffit juste de charger un csv, et d'observer les résultats <i class="glyphicon glyphicon-stats" aria-hidden="true"></i>. Attention, selon le nombre de lignes et de colonnes de votre Dataset, le temps de traitement peut d'être très long! <i class="glyphicon glyphicon-time" aria-hidden="true"></i></p>
	  </div>
	"""
	return my_alert

def alert_warning():
	my_alert = """
	<!-- SCRIPT CDN -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
	<!-- Alerte -->
	<div class="alert alert-warning" role="alert">
    	Le rapport a été généré dans un nouvel onglet de votre navigateur!
    </div>
	"""
	return my_alert