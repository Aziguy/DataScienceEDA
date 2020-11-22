# HTML render

def entete_de_page():
	my_header = """
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
	  <!-- Code for the jumbotron and modal class -->
	  <div class="jumbotron">
  		<h1 class="display-4">Google PlayStore</h1>
  		<p class="lead">Exploratory Data Analysis (EDA) & Machine learning</p>
  		<hr class="my-4">
  		<p>Cette application met en exergue l'analyse exploiratoire du dataset contenant l'ensemble des applications androids issue du play store. Cette base contient 13 colonnes parmi lesquelles nous pouvons citer : catergory, rating, size, etc. La variable à expliquer (target) ici est <b>Rating</b></p>
  		<button type="button" class="btn btn-primary btn-lg" data-toggle="modal" data-target="#myModal"><i class="glyphicon glyphicon-eye-open" aria-hidden="true"></i> Voir Détails </button>
      	<!-- The Modal -->
  		<div class="modal fade" id="myModal">
    		<div class="modal-dialog">
      			<div class="modal-content">
        		<!-- Modal Header -->
        			<div class="modal-header">
          				<h4 class="modal-title">Détails du jeux de données</h4>
          				<button type="button" class="close" data-dismiss="modal">&times;</button>
        			</div>
        		<!-- Modal body -->
        			<div class="modal-body">
          				<p><b>App :</b> Nom de l'application.</br>
          				<b>Category :</b> Catégorie d'appartenance de chaque application.</br>
          				<b>Rating :</b> Note attribué à chaque application (de 1.0 à 5.0).</br>
          				<b>Reviews :</b> Nombre de commentaire sur l'application.</br>
          				<b>Size :</b> Taille de l'application (en Mb).</br>
          				<b>Installs :</b> Nombre de fois que l'application a été installé.</br>
          				<b>Type :</b> Application payante ou gratuite.</br>
          				<b>Price :</b> Prix de l'application.</br>
          				<b>Content rating :</b> Cible de l'application (Tout le monde, Enfants, Adult, ...</br>
          				<b>Genres :</b> Le genre de l'application.</br>
          				<b>Last updated :</b> Dernière mise à jour de l'application.</br>
          				<b>Current Ver :</b> Version de l'application disponible dans le PlayStore.</br>
          				<b>Android Ver :</b> Version minimum d'android pour l'installation de l'application.
          				</p>
        			</div>
        		<!-- Modal footer -->
        			<div class="modal-footer">
          				<button type="button" class="btn btn-danger" data-dismiss="modal">Fermer</button>
        			</div>
      			</div>
    		</div>
  		</div>
      </div>
      <!-- END of The Modal -->
      <!-- Code for the blockquote -->
      <blockquote class="blockquote text-center">
  		<p class="mb-0">Team data analytics | data scientist en devenir.</p>
  		<footer class="blockquote-footer">Parce que vous <cite title="Source Title">êtes unique</cite></footer>
	  </blockquote>
      <!-- Code for the first row card with image rounded -->
      <div class="container-fluid">
      <div class="row justify-content-center">
	      	<div class="card-deck">
	  			<!-- Code for the first card -->
	  			<div class="card" style="width: 18rem;">
	    			<img class="card-img-top rounded-circle img-fluid" src="https://media-exp1.licdn.com/dms/image/C4D03AQEBVt38g3B3rg/profile-displayphoto-shrink_200_200/0?e=1610582400&v=beta&t=FGc4F0Q2Mxb2UqMIWQdjVY-ekT980AxJY4ztpjM3e0M" alt="...">
	    			<div class="card-body">
	      				<h5 class="card-title">Esteban Bara</h5>
	      				<p class="card-text">Integer pretium vel ex eu iaculis. Etiam congue velit in semper elementum. Quisque in dapibus sem dapibus nam.</p>
	      				<a href="https://www.linkedin.com/in/esteban-bara/" target="_blank" class="btn btn-primary">Mon profil</a>
	    			</div>
	  			</div>
	  			<!-- Code for the second card -->
	  			<div class="card" style="width: 18rem;">
	    			<img class="card-img-top rounded-circle img-fluid" src="https://media-exp1.licdn.com/dms/image/C4D03AQGy8yFqIR9T7Q/profile-displayphoto-shrink_200_200/0?e=1610582400&v=beta&t=yAIhvxin6p0OOJxaqFsiUN0bU_Me97mKLuZ9eSZdAqY" alt="...">
	    			<div class="card-body">
	      				<h5 class="card-title">Gervais Kituanga</h5>
	      				<p class="card-text">Nullam in tristique sapien, a accumsan mi. Nulla efficitur sapien vel lorem pulvinar luctus. Nulla erat curae. Nulla erat curae.</p>
	      				<a href="https://www.linkedin.com/in/gervais-kituanga-mitimiti/" target="_blank" class="btn btn-primary">Mon profil</a>
	    			</div>
	  			</div>
	  			<!-- Code for the third card -->
	  			<div class="card" style="width: 18rem;">
	    			<img class="card-img-top rounded-circle img-fluid" src="https://media-exp1.licdn.com/dms/image/C5603AQGR0FvgXG3Wpw/profile-displayphoto-shrink_200_200/0?e=1610582400&v=beta&t=ITFov0I8NubvPNuHHxc1c3j4-QiqglU0Nx7qS_sHNJM" alt="...">
	    			<div class="card-body">
	      				<h5 class="card-title">Thomas Touil</h5>
	      				<p class="card-text">Quisque sollicitudin enim sit amet urna porttitor pellentesque. Donec urna elit, hendrerit non mauris a fusce.</p>
	      				<a href="https://www.linkedin.com/in/thomas-touil-b168a5144/" target="_blank" class="btn btn-primary">Mon profil</a>
	    			</div>
	  			</div>
			</div>
	  </div>
	  </br>
	  <!-- Code for the second row card with image rounded -->
      <div class="row justify-content-center">
	      	<div class="card-deck">
	  			<!-- Code for the first card -->
	  			<div class="card" style="width: 18rem;">
	    			<img class="card-img-top rounded-circle img-fluid" src="https://www.w3schools.com/bootstrap4/img_avatar1.png" alt="...">
	    			<div class="card-body">
	      				<h5 class="card-title">Abdou Aziz Ziza</h5>
	      				<p class="card-text">Vivamus tincidunt nulla ac aliquet scelerisque. Praesent a lacus urna. Mauris libero dolor...</p>
	      				<a href="#" target="_blank" class="btn btn-primary">Mon profil</a>
	    			</div>
	  			</div>
	  			<!-- Code for the second card -->
	  			<div class="card" style="width: 18rem;">
	    			<img class="card-img-top rounded-circle img-fluid" src="https://media-exp1.licdn.com/dms/image/C4D03AQG01Lpt4F1BXw/profile-displayphoto-shrink_200_200/0?e=1610582400&v=beta&t=qB5dH88GAvxqNZNsrOzftF7wma9raAUYoyXNS5o-8PA" alt="...">
	    			<div class="card-body">
	      				<h5 class="card-title">Hippolyte KENGNI</h5>
	      				<p class="card-text">Après moi c'est moi ; avant moi c'est toujours moi ; après après moi c'est le virage...</p>
	      				<a href="https://www.linkedin.com/in/hippolyte-kengni-%F0%9F%93%8A%F0%9F%93%88-984808198/" target="_blank" class="btn btn-primary">Mon profil</a>
	    			</div>
	  			</div>
			</div>
	  </div>
	</div>
	"""
	return my_header

def pied_de_page():
	my_footer = """
	<!-- CSS CDN -->
	  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
	  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
	   <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">
	   <style>
  		/*-- about --*/
		.about{
			position: relative;
		}
		h3.position {
		    position: absolute;
		    font-size: 60px;
		    font-weight: 800;
		    letter-spacing: 5px;
		    transform: rotate(90deg);
		    right: -2%;
		    top: 30%;
		    color: #333;
		}
		.about-right h4.main {
		    font-size: 24px;
		    text-transform: capitalize;
		    font-weight: 600;
		    margin: 1em 0;
		}
		.about-right {
		    padding: 3em;
		}
		.about-right p {
		    font-size: 16px;
		    color: #777;
		}
		a.abt-btn {
		    background: #2a5298;
		    border: 2px solid #2a5298;
		    text-transform: capitalize;
		    color: #fff;
		    padding: 10px 25px;
		    display: inline-block;
		    margin-top: 2em;
		    letter-spacing: 1px;
		    font-size: 15px;
		    font-weight: 600;
		}
		.about-right-inner h4 {
		    font-size: 24px;
		    text-transform: capitalize;
		    font-weight: 600;
		    line-height: 38px;
		}
		.about-right-inner p {
		    line-height: 28px;
		}
		.progress-one .progress {
		    height: 0.3rem;
		}
		.progress {
		    font-size: 0.75em;
		    line-height: 8em;
		    text-align: center;
		    background-color: #d6d9da;
		    border-radius: 0.25rem;
		    margin-bottom: 1em;
		}
		.about-right-inner h4.progress-tittle {
		    color: #888;
		    font-size: 0.85em;
		    text-transform: uppercase;
		    margin-bottom: .5em;
		    letter-spacing: 1px;
		    line-height: inherit;
		}
		/*-- //about --*/
		</style>
	 
	 	<!-- about -->
		<section class="about" id="about">
			<div class="container-fluid">
				<div class="row">
					<div class="col-lg-5 p-0">
						<img src="https://demo.w3layouts.com/demos_new/template_demo/23-03-2019/client-demo_Free/2146656123/web/images/about1.jpg" alt="" class="img-fluid" />
					</div>
					<div class="col-lg-6">
						<div class="about-right">
							<h4 class="main">Auctor sit amet aliquam vel, ulla amet.</h4>
							<p>Auctor sit amet aliquam vel, ullamcorper sit amet ligula. Vivamus suscipit tortor eget felis porttitor volutpat. Mauris blandit
							aliquet elit.</p>
							<div class="row mt-sm-5 mt-4 about-right-inner">
								<div class="col-sm-4 col-6 myphoto-sign text-center">
									<img src="https://demo.w3layouts.com/demos_new/template_demo/23-03-2019/client-demo_Free/2146656123/web/images/myphoto.jpg" alt="" class="img-fluid rounded-circle"/>
									<img src="https://demo.w3layouts.com/demos_new/template_demo/23-03-2019/client-demo_Free/2146656123/web/images/signature.png" alt="" class="img-fluid mt-3"/>
									<a href="http://www.ingemedia.net/formation/master/data-analytics-strategie-information" target="_blank" class="scroll abt-btn">Hire Us </a>
								</div>
								<div class="col-sm-7 offset-lg-1">
									<h4>Personal Info</h4>
									<p>Hello, Our name is <strong>Group I </strong>. We have 10 years experienced <strong>BerceauMaqique</strong></p>
									<h4 class="mt-4">Skills & Abilities</h4>
									<div class="progress-one mt-3">
										<h4 class="progress-tittle">Data Analytics</h4>
										<div class="progress">
											<div class="progress-bar" role="progressbar" style="width: 80%" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100"></div>
										</div>
									</div>
									<div class="progress-one my-lg-3">
										<h4 class="progress-tittle">Data Visualisation</h4>
										<div class="progress">
											<div class="progress-bar bg-danger" role="progressbar" style="width: 65%" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100"></div>
										</div>
									</div>
									<div class="progress-one">
										<h4 class="progress-tittle">Machine learning</h4>
										<div class="progress">
											<div class="progress-bar bg-info" role="progressbar" style="width: 100%" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<h3 class="position">About Us</h3>
				</div>
		    </div>
		</section>
		<!-- //about -->
	"""
	return my_footer