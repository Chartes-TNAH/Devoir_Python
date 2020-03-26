import os
import csv
from lxml import etree
from tqdm import tqdm

Path = "./cache2019/cacheXML/"
Path_output = "./cache2019/cacheTXT/"
filelist = os.listdir(Path)
if not os.path.exists("./cache2019/cacheTXT"):
    os.makedirs("./cache2019/cacheTXT")
number = 1
dict_noms_abstract = {}
for abstract in tqdm(filelist):
    if abstract.endswith(".xml"):
        titre = abstract
        titre = titre.replace(".xml", "")
        titre = titre.replace("_", " ")
        try:
            with open(Path + abstract, "r", encoding="UTF-8") as y:
                tree = etree.parse(y)
                notags = etree.tostring(tree, encoding='utf8', method='text')
                year = 2019
                abstract = "paper-{0}-{1}.txt".format(year, number)
                input_name = abstract
                input_name = input_name.replace(".txt", "")
                notags = notags.decode('UTF-8')
                liste_mots = notags.split()
                texte = ' '.join(liste_mots)
                dict_noms_abstract[titre] = input_name
                with open(Path_output + abstract, "w", encoding="UTF-8") as z:
                    z.write(str(titre))
                    z.write(str(texte))
                number += 1
        except Exception:
            raise
            pass

with open('./cache2019/TEI2019.csv', 'r') as csvinput:
    with open('./cache2019/TEI2019-2.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)
        ensemble_du_document = []
        for row in reader:
            if row[2] in dict_noms_abstract:
                row.append(dict_noms_abstract[row[2]])
                ensemble_du_document.append(row)
        writer.writerows(ensemble_du_document)

if os.path.exists('./cache2019/TEI2019.csv'):
    os.remove('./cache2019/TEI2019.csv')
else:
    print("Fichier inexistant")

if os.path.exists('./cache2019/TEI2019-2.csv'):
    os.rename('./cache2019/TEI2019-2.csv', './cache2019/TEI2019.csv')
else:
    print("Fichier inexistant")
