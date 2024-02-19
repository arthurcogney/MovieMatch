# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 15:23:20 2022

@author: arthurc
"""


# Import Pandas
import pandas as pd
from ast import literal_eval
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from urllib.request import urlopen
import json


from PIL import Image
from io import BytesIO

import random


def real_film(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name'] #retourne le nom du réalisateur si il existe
    return np.nan               #sinon retourne tableau NaN


def liste_credits(x): #Cherche les personnes les plus importantes du film        
    if isinstance(x, list):
        nom = [i['name'] for i in x]
        if len(nom) > 3: #regarde si plus de 3 élements existe si c'est le cas il les retourne
            nom = nom[:3]
        return nom #sinon retourne la liste
    else:
        return [] #retourne un tableau vide si erreur
    
def nettoie(x): # Fonction qui supprime les espaces dans les mots et on transforme les mots en minuscule, permet ensuite la vectorization des mots
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x] 
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
        
def joindre_mots(x): # Cette fonction va permettre de choisir les elements importants à la comparaison des films
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])+ ' ' + x['director']
    #Il y a deux fois 'director' cela permet de mettre plus d'importance au réalisateur du film

# Importe la liste principal des films dans filmdata /// CHEMIN DE SAUVEGARDE A MODIFIER SELON ORDI
filmdata = pd.read_csv('C:/Users/skanh/Desktop/Projet_S6/Projet_Logiciel/ml-latest/base/movies_metadata.csv', low_memory=False)
# Importe la liste des credits dans acteurs
acteurs = pd.read_csv('C:/Users/skanh/Desktop/Projet_S6/Projet_Logiciel/ml-latest/base/credits.csv')
# Importe les motsclefs difinissant le film
motsclefs = pd.read_csv('C:/Users/skanh/Desktop/Projet_S6/Projet_Logiciel/ml-latest/base/keywords.csv')


filmdata = filmdata.drop([19730, 29503, 35587]) # On retire les donnees indésirable 
print(filmdata.shape) # Taille du tableau avant traitement
# On retire des films afin de faire moins de calcul d'eviter de recommender de mauvais films
moyenne_nbvote = filmdata['vote_count'].quantile(0.5) # On cherche 50% des films les moins voté (les moins populaires)
filmdata = filmdata.copy().loc[filmdata['vote_count'] >= moyenne_nbvote] # Puis on les supprime de la base pour faire moins de calcul
moyenne_vote = filmdata["vote_average"].quantile(0.3) # On cherche 30% des films les moins bien noté
filmdata = filmdata.copy().loc[filmdata['vote_average'] >= moyenne_vote] # Puis on les supprime aussi
print(filmdata.shape) # Taille du tableau après traitement


# On retire les éléments vides
filmdata['overview'] = filmdata['overview'].fillna('')

# On créer un indice pour chaque film avec de pouvoir les énumérés dans la base, on retire les duplicata
indices = pd.Series(filmdata.index, index=filmdata['title']).drop_duplicates()
filmdata['id'] = filmdata['id'].astype('int') # On converti les id des films en type int afin de faire un traitement
acteurs['id'] = acteurs['id'].astype('int')
motsclefs['id'] = motsclefs['id'].astype('int')

filmdata = filmdata.merge(acteurs, on='id') # Après avoir converti en int on fusionne acteurs avec la base de données principale
filmdata = filmdata.merge(motsclefs, on='id') # Pareil avec le tableau des mots clefs


donnees = ['cast', 'crew', 'keywords', 'genres'] # Liste des 4 données importante
for element in donnees:
    filmdata[element] = filmdata[element].apply(literal_eval) # On applique literal_eval afin d'évaluer les chaines de caractères
    
    
filmdata['director'] = filmdata['crew'].apply(real_film) # On défini le réalisteur du film grace à la fonction real_film
donnees = ['cast', 'keywords', 'genres']
for element in donnees:
    filmdata[element] = filmdata[element].apply(liste_credits) # Permet d'avoir les différentes donnees les plus importantes du film
        
donnees = ['cast', 'keywords', 'director', 'genres']

for element in donnees:
    filmdata[element] = filmdata[element].apply(nettoie) # On utilise la fonction nettoie pour ensuite analyser les données


filmdata['joint'] = filmdata.apply(joindre_mots, axis=1) # On applique joindre_mots pour pouvoir ensuite comparer les films   


# On fait une vectorization cela va permettre de faire des mesures statistiques sur le document
# On retire les "stop words" les mots simple comme 'a' 'the' 'of' etc...
vecto = CountVectorizer(stop_words='english')
# On converti le document en une matrice pour pouvoir traiter l'information
vecto_matrix = vecto.fit_transform(filmdata['joint'])

cosinus = cosine_similarity(vecto_matrix, vecto_matrix) # On cherche la similarité cosinus de tous les vecteurs (leur angle), permet de savoir si un film est proche d'un autre
filmdata = filmdata.reset_index() # Reset les indices de la base de données principale
indices = pd.Series(filmdata.index, index=filmdata['title'])

def recommendation(titre):
    film = indices[titre] # On cherche l'indice du film avec ce titre
    filmtest = indices["Frozen"]
    if(type(film) == type(filmtest)):
        film = film.iloc[-1] #Si il y a plusieurs films avec le même nom on prend le dernier dans la liste
    score_similitude = list(enumerate(cosinus[film])) # Cherche la similitude avec tous les films de la liste
    score_similitude = sorted(score_similitude, key=lambda x: x[1], reverse=True) # Classe les films celon le score de similitude
    score_similitude = score_similitude[0:filmdata.shape[0]] # On recupere le score des n films les plus similaire
    movie_indices = [i[0] for i in score_similitude] # Recupere les indices des films en questions
    return filmdata['title'].iloc[movie_indices] # Retourne les films

def calcul_moyenne(film1, film2, film3): # Fonction permet de trouver les films les plus hauts dans les 3 listes de films
    liste_film1 = []
    liste_film2 = []
    liste_film3 = []
    moyenne = []
    film_present = []
    for i in range(filmdata.shape[0]):  # On met dans la liste les différents films
        liste_film1.append(film1.iloc[i])
        liste_film2.append(film2.iloc[i])
        liste_film3.append(film3.iloc[i])
    #liste_film1 = filmdata['title'].tolist()
    #liste_film1 = filmdata['title'].tolist()
    #liste_film1 = filmdata['title'].tolist()
    for i in range(2000):
        for j in range(2000):
            if(liste_film2[j] == liste_film1[i]):
                for k in range(filmdata.shape[0]):
                    if(liste_film3[k] == liste_film2[j]):
                        moyenne.append((i+j+k)/3)   # On fait la moyenne de la position de tous les films recommandé
                        film_present.append(liste_film2[j]) # On affiche les film présents dans la liste moyenne 
    return moyenne, film_present

def top(moyenne, film): # Fonction permet de récupérer les 3 films avec la meilleure moyenne
    liste_moyenne, liste_film = (list(t) for t in zip(*sorted(zip(moyenne, film)))) # On trie la liste moyenne que l'on "synchronise" avec la liste film
    #la boucle permet de mettre l'objet tuple sous forme de liste
    return liste_film[0:8]


def poster(title): # Fonction qui permet de recuperer un poster à partir d'un titre
    url = 'https://omdbapi.com/?t=' + title.replace(' ','+') + '&apikey=1e341a53' # Utilise l'api omdb une base de données en ligne
    # ATTENTION : Api gratuite, pas plus de 1000 requêtes par jours
    response = urlopen(url) # On recupere les données depuis l'url
    data_json = json.loads(response.read()) # Donne un dictionnaire JSON
    url_poster = data_json["Poster"] # Url du poster
    image = urlopen(url_poster).read()
    #image = requests.get(url_poster, stream=True)
    poster_image = Image.open(BytesIO(image))
    return poster_image # Affichage de l'image

                
def movie_finder(film1,film2,film3):
    reco1 = recommendation(film1) # On stocks les 3 listes avec les recommendation selon les films
    reco2 = recommendation(film2)
    reco3 = recommendation(film3)
    moy, film = calcul_moyenne(reco1,reco2,reco3) # liste des films avec leurs score de présence (moyenne)
    top_film = top(moy, film) # On trie les films selon leur score et retournons les 10 les plus pertinents
    film_duplicata = []
    for i in range(len(top_film)): 
        url = 'https://omdbapi.com/?t=' + top_film[i].replace(' ','+') + '&apikey=1e341a53'
        response = urlopen(url)
        data_json = json.loads(response.read())
        
        if(top_film[i] == film1 or top_film[i] == film2 or top_film[i] == film3): # Si un des films est le même que un des trois entrées, nous le supprimons
            film_duplicata.append(top_film[i])
        if(data_json['Response'] == 'False' or top_film[i] in film_duplicata): # Si le film ne possède pas de poster nous le supprimons
            film_duplicata.append(top_film[i])
    for i in range(len(film_duplicata)):
        top_film.remove(film_duplicata[i])
    popularite = []
    id_film = []
    for i in range(len(top_film)):
        id_i = filmdata.loc[filmdata['title'] == top_film[i]]['id'].iloc[-1] # Cherche les id des films recommendés
        id_film.append(id_i)
    for i in range(len(top_film)):
        pop_i = filmdata.loc[filmdata['id'] == id_film[i]]['vote_count'] # Puis nous stockons le nombre de vote des films
        popularite.append(pop_i.iloc[0])
    popularite, top_film = (list(t) for t in zip(*sorted(zip(popularite, top_film), reverse=True))) # Nous trions les films selon le nombre de vote (leur popularité)   
    #Cela permet de ne pas recommender des films introuvable ou non connus
    return top_film[0:3] #On return les 3 films les plus pertinents

def top200_random(): # Une simple fonction où l'ont rend aléatoirement un film parmis les 300 les plus populaires
    liste_film = filmdata['title'].tolist()
    liste_vote = filmdata['vote_count'].tolist()
    liste_vote, liste_film = (list(t) for t in zip(*sorted(zip(liste_vote, liste_film), reverse=True))) # On trie les films selon leur nombre de vote dans la base de données
    return liste_film[random.randint(0,300)]
        



