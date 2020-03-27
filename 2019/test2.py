# Access each file in the corpus.
for infile in sorted(newcorpus.fileids()):
    print(infile) # The fileids of each file.
    with newcorpus.open(infile) as fin: # Opens the file.
        print(fin.read().strip()) # Prints the content of the file


# Access the plaintext; outputs pure string/basestring.
print(newcorpus.raw().strip())

# Access paragraphs in the corpus. (list of list of list of strings)
# NOTE: NLTK automatically calls nltk.tokenize.sent_tokenize and
#       nltk.tokenize.word_tokenize.
#
# Each element in the outermost list is a paragraph, and
# Each paragraph contains sentence(s), and
# Each sentence contains token(s)
print(newcorpus.paras())

# To access pargraphs of a specific fileid.
print(newcorpus.paras(newcorpus.fileids()[0]))

# Access sentences in the corpus. (list of list of strings)
# NOTE: That the texts are flattened into sentences that contains tokens.
print(newcorpus.sents())

# To access sentences of a specific fileid.
print(newcorpus.sents(newcorpus.fileids()[0]))

# Access just tokens/words in the corpus. (list of strings)
print(newcorpus.words())

# To access tokens of a specific fileid.
print(newcorpus.words(newcorpus.fileids()[0]))



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


model = Pipeline([
    ('norm', TextNormalizer()),
    ('vect', OneHotVectorizer()),
    ('clusters', KMeansClusters(k=7)),
])

