import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TextProcessor:
    def __init__(self):
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

    def tokenize(self, text):
        return nltk.word_tokenize(text)

    def remove_stopwords(self, tokens):
        return [word for word in tokens if word not in self.stop_words]

    def process_text(self, text):
        tokens = self.tokenize(text)
        return self.remove_stopwords(tokens)

    def lemmatize(self, tokens):
        stemmer = nltk.stem.WordNetLemmatizer()
        return [stemmer.lemmatize(token) for token in tokens]

    """"""
    def tfidf_cosim(self, doc, query):
        query = [query]
        tf = TfidfVectorizer(use_idf=True, sublinear_tf=True)
        tf_doc = tf.fit_transform(doc)
        tf_query = tf.transform(query)
        cosine_similarities = cosine_similarity(tf_doc,tf_query).flatten()
        most_similar_index = cosine_similarities.argsort()[:-2:-1]

        # Return the index of the most similar document and the cosine similarity value
        results = [most_similar_index[0], cosine_similarities[most_similar_index]]
        return results