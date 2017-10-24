import nltk
from nltk.corpus import stopwords
import re
import string
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn import metrics
import pandas as pd
import numpy as np
 
stemmer = PorterStemmer()
 
file = open("test-documents.txt", "r")
corpus = file.read()
corpus = corpus.split("\n")  
 
texts=[]
for i in range(len(corpus)):
    texts.append(corpus[i])
    texts[i] = texts[i].translate(string.punctuation).lower()
    texts[i] = nltk.word_tokenize(texts[i])
    texts[i] = [stemmer.stem(word) for word in texts[i] if not word in stopwords.words('english')]
    texts[i] = " ".join(texts[i])
 
transformer = TfidfVectorizer()
tfidf = transformer.fit_transform(texts)  

	
svd = TruncatedSVD(n_components = 2, algorithm='randomized')
lsa = svd.fit_transform(tfidf.T)

def getClosestTerm(term,transformer,model):
 
    term = stemmer.stem(term)
    index = transformer.vocabulary_[term]      
 
    model = np.dot(model,model.T)
    searchSpace =np.concatenate( (model[index][:index] , model[index][(index+1):]) )  
 
    out = np.argmax(searchSpace)
 
    if out<index:
        return transformer.get_feature_names()[out]
    else:
        return transformer.get_feature_names()[(out+1)]
 
def kClosestTerms(k,term,transformer,model):
 
    term = stemmer.stem(term)
    index = transformer.vocabulary_[term]
 
    model = np.dot(model,model.T)
 
    closestTerms = {}
    for i in range(len(model)):
        closestTerms[transformer.get_feature_names()[i]] = model[index][i]
 
    sortedList = sorted(closestTerms , key= lambda l : closestTerms[l])
 
    return sortedList[::-1][0:k]

print(getClosestTerm("beautiful",transformer,lsa))

print(kClosestTerms(5,"dawn",transformer,lsa))