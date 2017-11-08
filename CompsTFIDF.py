import numpy as np
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer

stop_Words = text.ENGLISH_STOP_WORDS

emails = pd.read_pickle("data/parsed/pickles/pickled_data_test.pickle")

def build_TFIDF_Matrix(df):
    vectorizer = TfidfVectorizer(stop_words = stop_Words)
    vectorized = vectorizer.fit_transform(df["Message-Contents"])

    dumb_numbers = [s for s in vectorizer.get_feature_names()
    if (("0" in s) or ("1" in s) or ("2" in s) or ("3" in s) or ("4" in s)
    or ("5" in s) or ("6" in s) or ("7" in s) or ("8" in s) or ("9" in s) or ("_" in s))]

    stop_words = text.ENGLISH_STOP_WORDS.union(dumb_numbers)

    vectorizer = TfidfVectorizer(stop_words = stop_words)
    vectorized = vectorizer.fit_transform(df["Message-Contents"])
    return vectorizer, vectorized





#vectorizer = TfidfVectorizer(stop_words = stop_Words)
#vectorized = vectorizer.fit_transform(our_Corpus)

#print(vectorized.shape)
#print(vectorized)
#print(vectorized.toarray())
##print(vectorizer.idf_)
#print(vectorizer.get_feature_names())
#
# for i in range(vectorized.shape[0] - 1):
#     print(our_Corpus[i])
#     for j in range(len(vectorizer.get_feature_names())):
#         print(vectorizer.get_feature_names()[j], vectorized.toarray()[i][j])
