# Objectif #

Ce programme permet de faire de l'analyse textuelle à partir des abstracts des TEI CONFERENCE de certaines années. Chaque dossier nommé d'après une année permet d'analyser cette année précise.

# Fonctionnement #

Il faut entrer dans le dossier de l'avant souhaité, installer un environnement virtuel dans le dossier de l'année (par exemple : .//2019/ ) avec la commande :  virtualenv -p python3 venv 
Ensuite, il faut installer toutes les dépendances mentionnées dans le dossier requirements.txt grâce à la commande " pip install -r requirements.txt ".

Vous pouvez maintenant lancer votre jupyter notebook. Il faudra alors lancer **dans l'ordre** :
- Download.ipynb
- Normalisation des documents.ipynb
- Analyse textuelle et clustering.ipynb



Enjoy :) 

