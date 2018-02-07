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
    else:
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
    else:
        scenario_1_test = pd.DataFrame(df[2::3])
    matrix_test = CompsTFIDF.build_test_tfidf(vectorize, scenario_1_test)
    np.save('test_scenario_1_tfidf.npy', matrix_test)
    return matrix_test


def discoverEnron(sceaniroNum):
    #Train data cleaned
    email_clean_train = cleanData("./data/parsed/training.csv")
    print("Train Emails Cleaned")
    
    #Test data cleaned
    email_clean_test = cleanData("./data/parsed/test.csv")
    print("Test Emails Cleaned")
    
    #TFIDF Run for Train data
    tfidf_train_vectorizer, tfidf_train_matrix = tfidfData(email_clean_train, scenarioNum)
    np.save("train_tfidf_1.npy", tfidf_train_matrix)
    print("Train TFIDF Matrix Done")

    #TFIDF Run for Test data
    tfidf_test_matrix = testTFIDF(tfidf_train_vectorizer, email_clean_test,scenarioNum)
    np.save("test_tfidf_1.npy", tfidf_test_matrix)
    print("Test TFIDF Matrix Done")

    #LSA build for train emails
    CompsLSA.build_LSA_train_test(tfidf_test_matrix, tfidf_train_matrix)
    print("Train/Test LSA Complete")

    #Split Email Data based on inputted scenario
    if scenarioNum == 1:
        train_email_full = pd.DataFrame(email_clean_train[0::3])
        test_email_full = pd.DataFrame(email_clean_test[0::3])
    elif scenarioNum == 2:
        train_email_full = pd.DataFrame(email_clean_train[1::3])
        test_email_full = pd.DataFrame(email_clean_test[1::3])
    else:
        train_email_full = pd.DataFrame(email_clean_train[2::3])
        test_email_full = pd.DataFrame(email_clean_test[2::3])

    #Combine LSA and Email Data (TRAIN)
    full_train_df = CompsML.setup_dataframe('lsa_output_train_Feb8.npy', train_email_full)
    print("Train LSA/DF built")
    
    #Combine LSA and Email Data (TEST)
    full_test_df = CompsML.setup_dataframe('lsa_output_test_Feb8.npy', test_email_full)
    print("Test LSA/DF built")

    #Train Tree on full_train_df
    CompsML.train_tree(full_train_df)
    print("Tree Trained")

    #Run Evaluation on Test Emails
    CompsML.test_tree('scenario_full_train.pickle', full_test_df)


discoverEnron(1)
