# Changelog

Toutes les évolutions notables sont consignées ici. Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versionnage [SemVer](https://semver.org/lang/fr/).

## [2.0.0] - 2026-10-29

### Ajouté

- Package `playstore_insights` (layout `src/`) avec CLI `playstore-insights`.
- Nettoyage reproductible depuis le CSV brut et rapport de qualité.
- Modèle de notation par gradient boosting, comparé à 4 alternatives en validation croisée.
- Classifieur de sentiment TF-IDF et régression logistique.
- Export JSON des modèles et runtime JavaScript, parité testée avec Python.
- Site statique GitHub Pages : tableau de bord, exploration, sentiment, modèle, méthodologie.
- Badges de couverture et de performance auto-hébergés.
- CI (lint, tests Python 3.10 à 3.13, build Docker), Dependabot, pre-commit.
- Dockerfile, Makefile, documentation de contribution.

### Modifié

- Application Streamlit réécrite en multipage avec les API actuelles.
- Dépendances réduites de 140 paquets figés à 4 dépendances principales.

### Supprimé

- Intégrations D-Tale et pandas-profiling, remplacées par un profileur CSV natif.
- CSV pré-nettoyé non reproductible et rapport Sweetviz généré.

## [1.0.0] - 2020-11-15

- Première version : application Streamlit, EDA et modèle KNN.
