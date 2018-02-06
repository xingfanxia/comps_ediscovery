import email_filter
import CompsTFIDF
import CompsLSA
import CompsML
import numpy as np
import pandas as pd

#Input: data path as string of data in csv form
#Ouput: pandas dataframe of cleaned data
#Input data will be filterd for TFIDF and LSA. A pickled version of the  data  will be saved
def cleanData(datapath):
    df = pd.read_csv(datapath, dtype=str)

    email_filtered = pd.DataFrame()
    email_filtered = email_filter.full_filter_email(df)

    return email_filtered


#Input: pandas data frame of cleaned data
#Ouput: list of feature names in [0] and tfidf matrix in [1]
#Create tfidf matrix from cleaned train data. Save copy of matrix as well
def tfidfData(emaildf, scenarioNum):
    if scenarioNum == 1:
        scenario_1 = pd.DataFrame(emaildf[0::3])
    elif scenarioNum == 2:
        scenario_1 = pd.DataFrame(emaildf[1::3])
    else scenarioNum == 3:
        scenario_1 = pd.DataFrame(emaildf[2::3])
    scenario_1_tfidf_matrix = CompsTFIDF.build_TFIDF_Matrix(scenario_1)
    vectorizer = scenario_1_tfidf_matrix[0]
    scenario_1_tfidf = scenario_1_tfidf_matrix[1].toarray()
    np.save('scenario_1_tfidf.npy', scenario_1_tfidf)

    return vectorizer, scenario_1_tfidf


#Input: Training set TFIDFVectorizer (tfidfData[0] output), pandas data frame of cleaned test data
#Output: tfidf matrix of test data
#Create tfidf matrix from cleaned test data using train tfidf vectorizer. Save copy of matrix as well
def testTFIDF(vectorize, df, scenarioNum):
    if scenarioNum == 1:
        scenario_1_test = pd.DataFrame(df[0::3])
    elif scenarioNum == 2:
        scenario_1_test = pd.DataFrame(df[1::3])
    else scenarioNum == 3:
        scenario_1_test = pd.DataFrame(df[2::3])
    matrix_test = CompsTFIDF.build_test_tfidf(vectorize, scenario_1_test)
    np.save('test_scenario_1_tfidf.npy', matrix_test)
    return matrix_test


#Input: tfidfMatrix ([1]output from tfidfData())
#Output: No direct ouput. Pickled LSA matrix
def lsaData(tfMatrix):
    lsa_email = CompsLSA.build_LSA_Matrix(tfMatrix)
    #NEEDS TO BE SAVED .NPY USING MORE RAM COMPUTER
    return lsa_email



def discoverEnron(sceaniroNum):
    #Train data cleaned and TFIDF Run
    email_clean_train = cleanData("training.csv")
    print("Train Emails Cleaned")
    tfidf_train_vectorizer, tfidf_train_matrix = tfidfData(email_clean_train, scenarioNum)
    np.save("train_tfidf_1.npy", tfidf_train_matrix)
    print("Train TFIDF Matrix Done")

    #Test Data cleaned and TFIDF build
    email_clean_test = cleanData("test.csv")
    print("Test Emails Cleaned")
    email_tfidf_test = testTFIDF(tfidf_train_vectorizer, email_clean_test,scenarioNum)
    np.save("test_tfidf_1.npy", email_tfidf_test)
    print("Test TFIDF Matrix Done")

    #LSA build for train emails
    # email_lsa_train = lsaData(email_tfidf_train_matrix)
    # print("Train LSA Matrix Done")
    CompsLSA.build_LSA_train_test(email_tfidf_test, tfidf_train_matrix)
    print("Train/Test LSA Complete")

discoverEnron(1)
