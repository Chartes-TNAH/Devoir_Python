import os
from lxml import etree

Path = "./cache2019/cacheXML/"
Path_output = "./cache2019/cacheTXT/"
filelist = os.listdir(Path)
if not os.path.exists("./cache2019/cacheXML"):
    os.makedirs("./cache2019/cacheTXT")
for abstract in filelist:
    if abstract.endswith(".xml"):
        try:
            with open(Path + abstract, "r", encoding="UTF-8") as y:
                tree = etree.parse(y)
                notags = etree.tostring(tree, encoding='utf8', method='text')
                abstract = abstract.replace(".xml", ".txt")
                notags = notags.decode('UTF-8')
                notags = notags.replace("\n", " ")
                with open(Path_output + abstract, "w", encoding="UTF-8") as z:
                    z.write(str(notags))
        except:
            pass