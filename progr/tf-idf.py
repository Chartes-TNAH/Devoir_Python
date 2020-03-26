from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import os
Path = "./cache2019/cacheTXT/"
filelist = os.listdir(Path)

documents = []
for abstract in filelist:
    with open(Path + abstract, "r", encoding="UTF-8") as y:
        y = y.read()
        documents.append(y)

#vectorize the text i.e. convert the strings to numeric features
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

#cluster documents, ici 10 clusters
true_k = 10
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

#print top terms per cluster clusters
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i)
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])
