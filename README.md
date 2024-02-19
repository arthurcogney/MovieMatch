![MovieMatch](https://github.com/arthurcogney/MovieMatch/assets/95025754/73699ba7-4e27-446b-9bfe-1b3dfa5e81c1)

### Movie Match 2021 - 2022

## Les bibliothèques nécessaires
pandas
ast
sklearn
urllib
json
PIL
io
random
tkinter

## La base de donnée nécessaire
Télécharger la base de donnée movie lens:
https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

## Comment utiliser le programme
Editer le fichier main_movie_finder.py:
	Changer le chemin de destination des fichiers de la base de donnée
	'movies_metadata.csv'
	'credits.csv'
	'keywords.csv'
Compiler le fichier graphique.py
Cliquer sur start puis liker ou non les différents films

![Screenshot_3](https://github.com/arthurcogney/MovieMatch/assets/95025754/01d41c8e-542b-432c-951d-5d75ac8a7681)

## Problèmes potentiels
- L'api pour récupérer les poster est gratuite et limité à 1000 requêtes/jours/clé,
  si l'utilisateur fait trop de requêtes il est possible que les poster ne s'affiche plus.
  Il faut utiliser une nouvelle clé et la changer directement dans le programme (ou attendre...)
- Le temps de compilation peut être long, afin de le réduire nous pouvons modifier la ligne suivante :
	moyenne_nbvote = filmdata['vote_count'].quantile(0.5)
  En augmentant le quantile afin de faire les calculs pour moins de film, par exemple : 
	moyenne_nbvote = filmdata['vote_count'].quantile(0.8)
- Il est possible que certains films n'aient pas de poster correspondant une page blanche va donc s'afficher.
