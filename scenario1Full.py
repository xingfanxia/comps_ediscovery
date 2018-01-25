import email_filter
import CompsTFIDF
import CompsLSA
import numpy as np
import pandas as pd

#Input: data path as string of data in csv form
#Ouput: pandas dataframe of cleaned data
#Input data will be filterd for TFIDF and LSA. A pickled version of the  data  will be saved
def cleanData(datapath):
    df = pd.read_csv(datapath, dtype=str)
    
    email_filtered = pd.DataFrame()
    email_filtered = email_filter.full_filter_email(df)
    #This is causing problems
#    email_filtered.to_pickle("filtered_email.pickle")
    
    return email_filtered


#Input: pandas data frame of cleaned data
#Ouput: list of feature names in [0] and tfidf matrix in [1]
#Create tfidf matrix from cleaned train data. Save copy of matrix as well
def tfidfData(emaildf):
    scenario_1 = df[emaildf["Scenario"] == '401']
    
    scenario_1_tfidf_matrix = CompsTFIDF.build_TFIDF_Matrix(scenario_1)
    feature_names = scenario_1_tfidf_matrix[0].get_feature_names()
    scenario_1_tfidf = scenario_1_tfidf_matrix[1].toarray()
    np.save('scenario_1_tfidf.npy', scenario_1_tfidf)
    
    return vectorizer, scenario_1_tfidf


#Input: Training set TFIDFVectorizer (tfidfData[0] output), pandas data frame of cleaned test data
#Output: tfidf matrix of test data
#Create tfidf matrix from cleaned test data using train tfidf vectorizer. Save copy of matrix as well
def testTFIDF(vectorize, df):
    scenario_1_test = df[df["Scenario"] == '401']
    matrix_test = CompsTFIDF.build_test_tfidf(vectorize,scenario_1_test)
    np.save('test_scenario_1_tfidf.npy', matrix_test)
    return matrix_test


#Input: tfidfMatrix ([1]output from tfidfData())
#Output: No direct ouput. Pickled LSA matrix
def lsaData(tfMatrix):
    lsa_email = CompsLSA.build_LSA_Matrix(tfMatrix)
    #NEEDS TO BE SAVED .NPY USING MORE RAM COMPUTER
    return lsa_email



def discoverEnron1():
    #Train data cleaned and TFIDF Run
    email_clean_train = cleanData("./data/parsed/training.csv")
    print("Train Emails Cleaned")
    email_tfidf_train_vectorizer, email_tfidf_train_matrix = tfidfData(email_clean)
    print("Train TFIDF Matrix Done")
    
    #Test Data cleaned and TFIDF build
    email_clean_test = cleanData("./data/parsed/test.csv")
    print("Test Emails Cleaned")
    email_tfidf_test = testTFIDF(email_tfidf_train_vectorizer,email_clean_test)
    
    #LSA build for train emails
    email_lsa_train = lsaData(email_tfidf_train_matrix)
    print("Train LSA Matrix Done")
    
    
    
