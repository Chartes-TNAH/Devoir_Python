from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import json

content = urlopen('https://gams.uni-graz.at/context:tei2019.papers?context=context:tei2019.papers')
HTML = content.read()


soup = BeautifulSoup(HTML, 'html.parser')
listLink = []
for link in soup.find_all('a'):
    if 'TEI_SOURCE' in link.get('href'):
        lien = link.get('href')
        listLink.append(lien)


with open('./cache2019/liste_des_liens_internet.json', 'w') as liste_des_liens_internet:
    i = 0
    liste_lien = {}
    for linky in listLink:
        lien = 'https://gams.uni-graz.at' + linky
        liste_lien[i] = lien
        i += 1
    json.dump(liste_lien, liste_des_liens_internet)

i = 0
with open('./cache2019/liste_des_liens_internet.json', 'r') as liste_des_liens_internet:
    dicoXML = {}
    liste_liens_lisible = liste_des_liens_internet.read()
    dico_liens = json.loads(liste_liens_lisible)
    for link in dico_liens:
        lien = dico_liens[link]
        XML = urlopen(lien).read()
        XML = XML.decode("UTF-8")
        dicoXML[i] = XML
        i += 1


        





with open('./cache2019/TEI2019.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    i = 0
    for key in dicoXML:
        value = dicoXML[i]
        soup = BeautifulSoup(value, 'xml')
        for elem in soup.name:
            nom = soup.forename.contents
            prenom = soup.surname.contents
        for elem in soup.publisher:
            orga = soup.orgName.contents
        for elem in soup.titleStmt:
            titre = soup.title.contents
        for elem in soup.keywords:
            liste_motcles = soup.find_all('term')
            retypage_liste = [str(i) for i in liste_motcles]
            motcles = str(" | ".join(retypage_liste))
            motcles = motcles.replace("<term>", "")
            motcles = motcles.replace("</term>", "")
            motcles = [motcles]
        abstract = soup("body")
        abstract = abstract[0]
        titre_dans_cache = titre[0]
        with open('./cache2019/cacheXML/%s.xml' % titre_dans_cache, 'w', encoding='UTF-8') as docXML:
            docXML.write(str(abstract))
        titre_dans_cache = titre_dans_cache + ".xml"
        masterList = prenom + nom + orga + titre + motcles
        writer.writerow(masterList)
        i += 1
        masterList = []


