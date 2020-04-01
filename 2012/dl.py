from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import json
import os
from tqdm import tqdm

content = urlopen('https://tei-c.org/Vault/MembersMeetings/2012/teiconference/program/papers/#mads')
HTML = content.read()

if not os.path.exists("./cache2012"):
    os.makedirs("./cache2012")
if not os.path.exists("./cache2012/cacheXML"):
    os.makedirs("./cache2012/cacheXML")

soup = BeautifulSoup(HTML, 'html.parser')
liste_des_abstracts = {}
i = 1
for hr in tqdm(soup.find_all("hr")):
    for item in tqdm(hr.find_next_siblings()):
        if item.name == "hr":
            break
        liste_des_abstracts[i] = item

print(liste_des_abstracts)


