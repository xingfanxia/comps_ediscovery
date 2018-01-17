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
    email_filtered.to_pickle("filtered_email.pickle")
    
    return email_filtered


#Input: pandas data frame of cleaned data
#Ouput: list of feature names in [0] and tfidf matrix in [1]
#Create tfidf matrix from cleaned data. Save copy of matrix as well
def tfidfData(emaildf):
    scenario_1 = df[emaildf["Scenario"] == '401']
    
    scenario_1_tfidf_matrix = CompsTFIDF.build_TFIDF_Matrix(scenario_1)
    feature_names = scenario_1_tfidf_matrix[0].get_feature_names()
    scenario_1_tfidf = scenario_1_tfidf_matrix[1].toarray()
    np.save('scenario_1_tfidf.npy', scenario_1_tfidf)
    
    return feature_names, scenario_1_tfidf


#Input: tfidfMatrix ([1]output from tfidfData())
#Output: No direct ouput. Pickled LSA matrix
def lsaData(tfMatrix):
    lsa_email = CompsLSA.build_LSA_Matrix(tfMatrix)
    #NEEDS TO BE SAVED .NPY USING MORE RAM COMPUTER
    return lsa_email



def discoverEnron1():
    email_clean = cleanData("./data/parsed/training.csv")
    print("Emails Cleaned")
    email_tfidf = tfidfData(email_clean)
    print("TFIDF Matrix Done")
    email_lsa = lsaData(email_tfidf[1])
    print("LSA Matrix Done")
    
    
