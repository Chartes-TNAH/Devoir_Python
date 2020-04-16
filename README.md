# Objectif #

Ce programme permet de faire de l'analyse textuelle à partir des abstracts des TEI CONFERENCE de certaines années (2012, 2016, 2019). Chaque dossier nommé d'après une année permet d'analyser cette année précise.

# Fonctionnement #

## Installation de l'environnement virtuel ##

Il faut installer votre environnement virtuel dans le dossier à la racine (./devoir_python), là où se trouve le requirements.txt, avec la commande :  virtualenv -p python3 venv 

Ensuite, il faut installer toutes les dépendances mentionnées dans le dossier requirements.txt grâce à la commande " pip install -r requirements.txt ".

***IMPORTANT***

Le corpus d'entraînement pour la lemmatisation de spacy peut ne pas s'installer via le requirements (temps d'attente trop long), il faudra donc si besoin ajouter en outre dans votre terminal, une fois votre environnement virtuel activé, la commande suivante :
- python -m spacy download en_core_web_sm
(et dans ce cas supprimer la dernière ligne du requirements : "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz" et relancer l'installation du requirements, car cela fera crasher l'installation de tous les autres packages)

Si cela ne fonctionne toujours pas, vous pouvez finalement tenter l'installation dans le Jupyter Notebook en créant une nouvelle cellule où vous écrirez puis activerez cela :
- pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz

## Sens de lecture ##

Vous pouvez maintenant lancer votre jupyter notebook. Il faudra alors lancer **dans l'ordre** les fichiers suivant l'ordre des "step" (step_1 puis step_2, etc...) indiqués dans le nom du fichier.



Enjoy :) 

