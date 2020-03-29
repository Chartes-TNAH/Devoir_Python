from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import json
import os
from tqdm import tqdm

content = urlopen('https://gams.uni-graz.at/context:tei2019.papers?context=context:tei2019.papers')
HTML = content.read()


soup = BeautifulSoup(HTML, 'html.parser')
listLink = []
print("Saisie des liens")
for link in tqdm(soup.find_all('a')):
    if 'TEI_SOURCE' in link.get('href'):
        lien = link.get('href')
        listLink.append(lien)

if not os.path.exists("./cache2019"):
    os.makedirs("./cache2019")
if not os.path.exists("./cache2019/cacheXML"):
    os.makedirs("./cache2019/cacheXML")


with open('./cache2019/liste_des_liens_internet.json', 'w') as liste_des_liens_internet:
    i = 0
    liste_lien = {}
    print("Stockage des liens")
    for linky in tqdm(listLink):
        lien = 'https://gams.uni-graz.at' + linky
        liste_lien[i] = lien
        i += 1
    json.dump(liste_lien, liste_des_liens_internet)

i = 0
with open('./cache2019/liste_des_liens_internet.json', 'r') as liste_des_liens_internet:
    dicoXML = {}
    liste_liens_lisible = liste_des_liens_internet.read()
    dico_liens = json.loads(liste_liens_lisible)
    print("Téléchargement en cours...")
    for link in tqdm(dico_liens):
        lien = dico_liens[link]
        XML = urlopen(lien).read()
        XML = XML.decode("UTF-8")
        dicoXML[i] = XML
        print("téléchargement accompli : {0}/46".format(i))
        i += 1
    print("Téléchargement terminé.")


with open('./cache2019/TEI2019.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    i = 0
    for key in dicoXML:
        value = dicoXML[i]
        soup = BeautifulSoup(value, 'xml')
        print("Récupération des autorités...")
        for contributeur in tqdm(soup.find_all('author')):
            for elem in soup.name:
                liste_noms_balise = soup.find_all(['forename', 'surname'])
                noms_a_rassembler = []
                for nom in liste_noms_balise:
                    nom = str(nom)
                    nom = nom.replace("<forename>", "")
                    nom = nom.replace('<forename full="yes">', "")
                    nom = nom.replace("</forename>", "")
                    nom = nom.replace("</surname>", "")
                    nom = nom.replace("<surname>", "")
                    nom = nom.replace('<surname full="yes">', "")
                    nom = nom.replace('<surname  full="init">', "")
                    nom = nom.replace('<forename full="init">', "")
                    nom = nom.replace('<forename full="abb">', "")
                    noms_a_rassembler.append(nom)
            for elem in soup.publisher:
                organisation = soup.orgName.contents
                orga = organisation[0].split()
                orga = ' '.join(orga)
                orga = [orga]
            for elem in soup.titleStmt:
                titre = soup.title.contents
                if len(titre) > 1:
                    titre = titre[0]
                    titre = [titre]
        print("Récupération des mots-clés...")
        for elem in tqdm(soup.keywords):
            liste_motcles = soup.find_all('term')
            retypage_liste = [str(i) for i in liste_motcles]
            motcles = str(" | ".join(retypage_liste))
            motcles = motcles.replace("<term>", "")
            motcles = motcles.replace("</term>", "")
            motcles = [motcles]
        abstract = soup("body")
        abstract = abstract[0]
        titre_dans_cache = titre[0]
        titre_dans_cache = titre_dans_cache.replace(" ", "_")
        with open('./cache2019/cacheXML/%s.xml' % titre_dans_cache, 'w', encoding='UTF-8') as docXML:
            docXML.write(str(abstract))
        titre_dans_cache = titre_dans_cache + ".xml"
        noms_rassembles = ' '.join(noms_a_rassembler)
        noms = [noms_rassembles]
        masterList = noms + orga + titre + motcles
        writer.writerow(masterList)
        i += 1
        masterList = []
