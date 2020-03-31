from typing import Any, Callable

import nltk
from nltk.cluster import KMeansClusterer
from numpy.core.multiarray import ndarray
from sklearn.base import BaseEstimator, TransformerMixin
import unicodedata
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

nltk.download('stopwords')


def is_punct(token):
    return all(unicodedata.category(char).startswith('P') for char in token)


class TextNormalizer(BaseEstimator, TransformerMixin):
    def __init__(self, language='english'):
        self.stopwords = set(nltk.corpus.stopwords.words(language))
        self.lemmatizer = nltk.WordNetLemmatizer()

    def is_stopword(self, token):
        return token.lower() in self.stopwords

    def normalize(self, document):
        return [
            self.lemmatize(token, tag).lower()
            for paragraph in document
            for sentence in paragraph
            for (token, tag) in sentence
            if not self.is_punct(token) and not self.is_stopword(token)
        ]

    def lemmatize(self, token, tag):
        pass

    def is_punct(self, token):
        pass

    def transform(self, documents):
        return [' '.join(self.normalize(doc)) for doc in documents]


class KMeansClusters(BaseEstimator, TransformerMixin):
    distance: Callable[[Any, Any], ndarray]

    def __init__(self, k=7):
        """
        k is the number of clusters
        model is the implementation of Kmeans
        """
        self.k = k
        self.distance = nltk.cluster.util.cosine_distance
        self.model = KMeansClusterer(self.k, self.distance, avoid_empty_clusters=True)


class OneHotVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.vectorizer = CountVectorizer(binary=True)

    def fit(self):
        return self

    def transform(self, documents):
        freqs = self.vectorizer.fit_transform(documents)
        return [freq.toarray()[0] for freq in freqs]


corpusdir = './cache2019/cacheTXT/'

newcorpus = PlaintextCorpusReader(corpusdir, '.*')
model = Pipeline([
    ('norm', TextNormalizer()),
    ('vect', OneHotVectorizer()),
    ('clusters', KMeansClusters(k=4)),
])

clusters = model.fit_transform(newcorpus)
pickles = list(newcorpus.fileids)

for idx, cluster in enumerate(clusters):
    print("Document '{}' assigned to cluster {}.".format(pickles[idx],cluster))