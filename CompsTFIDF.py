import numpy as np
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
stop_Words = text.ENGLISH_STOP_WORDS

#Input: Cleaned pandas dataframe of emails
#Ouput: [0] vectorizer used to build matrix, [1] tfidf matrix of data
#Build TFIDF matrix on given pandas data frame of cleaned emails
def build_TFIDF_Matrix(df):
    vectorizer = TfidfVectorizer(stop_words = stop_Words, min_df = .0005)
    vectorized = vectorizer.fit_transform(df["Message-Contents"])

    dumb_numbers = [s for s in vectorizer.get_feature_names()
    if (("0" in s) or ("1" in s) or ("2" in s) or ("3" in s) or ("4" in s)
    or ("5" in s) or ("6" in s) or ("7" in s) or ("8" in s) or ("9" in s) or ("_" in s) or (s == "ll"))]

    stop_words = text.ENGLISH_STOP_WORDS.union(dumb_numbers)

    vectorizer = TfidfVectorizer(stop_words = stop_words, min_df = .0005)
    vectorized = vectorizer.fit_transform(df["Message-Contents"])
    return vectorizer, vectorized


#Input: TFIDF vectorizer, Cleaned pandas dataframe of emails
#Ouput: tfidf matrix of data
#Build TFIDF matrix on given pandas data frame of cleaned emails with inputted tfidf vectorizer
def build_test_tfidf(vectorize, df):
    test_matrix = vectorize.transform(df)
    return test_matrix


#Input: tf_matrix = tfidf matrix, tf_vectorizer = TFIDF vectorizer, email_id = id's of all emails
#Ouput: pandas dataframe with columns being ID and all the feature names and then rows being the tfidf values
#Dataframe for intelligent searching
def tfidf_to_df(tf_matrix, tf_vectorizer, email_id):
    newDF = pd.DataFrame(tf_matrix, columns = tf_vectorizer.get_feature_names())
    newDF["ID"] = pd.Series(email_id)
    return newDF
