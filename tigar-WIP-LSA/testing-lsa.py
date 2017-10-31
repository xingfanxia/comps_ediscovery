import nltk
from nltk.corpus import stopwords
import re
import string
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn import metrics
import pandas as pd
import numpy as np
 
stemmer = PorterStemmer()

file = open("test-documents.txt", "r")
corpus = file.read()
corpus = corpus.split("\n") 

 
corpusList=[]
for i in range(len(corpus)):
    corpusList.append(corpus[i])
    corpusList[i] = corpusList[i].translate(string.punctuation).lower()
    corpusList[i] = nltk.word_tokenize(corpusList[i])
    corpusList[i] = [stemmer.stem(word) for word in corpusList[i] if not word in stopwords.words('english')]
    corpusList[i] = " ".join(corpusList[i])

#print(corpusList)
 
transformer = TfidfVectorizer()
tfidf = transformer.fit_transform(corpusList)  

svd = TruncatedSVD(n_components = 100, algorithm='randomized')
lsa = svd.fit_transform(tfidf.T)

print(lsa)

def getClosest(term,transformer,model):
 
    term = stemmer.stem(term)
    index = transformer.vocabulary_[term]      
 
    model = np.dot(model,model.T)
    searchSpace =np.concatenate( (model[index][:index] , model[index][(index+1):]) )  
    out = np.argmax(searchSpace)
    if out<index:
        return transformer.get_feature_names()[out]
    else:
        return transformer.get_feature_names()[(out+1)]
 
def kClosest(k,term,transformer,model):
 
    term = stemmer.stem(term)
    index = transformer.vocabulary_[term]
 
    model = np.dot(model,model.T)
 
    closestTerms = {}
    for i in range(len(model)):
        closestTerms[transformer.get_feature_names()[i]] = model[index][i]
 
    sortedList = sorted(closestTerms , key= lambda l : closestTerms[l])
 
    return sortedList[::-1][0:k]

print(getClosest("beautiful",transformer,lsa))

print(kClosest(5,"flower",transformer,lsa))