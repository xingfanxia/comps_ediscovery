import numpy as np
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer

stop_Words = text.ENGLISH_STOP_WORDS

our_Corpus = ["We 013 are 12:48 learning 894h08e5t23 NLP for our 23523 comps today 3462346.", "We 1345234 need to figure this NLP 23452346 out if we want 12/24/2107 our comps to work!", "Did anyone work 5 on the NLP for comps today?", "The weather 23523 is way too warm 5684567 today for mid-to-late October."]

#df = pd.read_csv("CompsExample.csv", sep=",", names = ['Content'])

vectorizer = TfidfVectorizer(stop_words = stop_Words)
vectorized = vectorizer.fit_transform(our_Corpus)
dumb_numbers = [s for s in vectorizer.get_feature_names() if (("0" in s) or ("1" in s) or ("2" in s) or ("3" in s) or ("4" in s) or ("5" in s) or ("6" in s) or ("7" in s) or ("8" in s) or ("9" in s))]
stop_words = text.ENGLISH_STOP_WORDS.union(dumb_numbers)
vectorizer = TfidfVectorizer(stop_words = stop_words)
vectorized = vectorizer.fit_transform(our_Corpus)

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
