from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

stop_Words = text.ENGLISH_STOP_WORDS

our_Corpus = ["We are learning NLP for our comps today.", "We need to figure this NLP out if we want our comps to work!", "Did anyone work on the NLP for comps today?", "The weather is way too warm today for mid-to-late October."]

vectorizer = TfidfVectorizer(stop_words = stop_Words)

vectorized = vectorizer.fit_transform(our_Corpus)

#print(vectorized.shape)
#print(vectorized)
print(vectorized.toarray())
#print(vectorizer.idf_)
print(vectorizer.get_feature_names())

for i in range(vectorized.shape[0]):
    print(our_Corpus[i])
    for j in range(len(vectorizer.get_feature_names())):
        print(vectorizer.get_feature_names()[j], vectorized.toarray()[i][j])

    
