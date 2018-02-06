#import forest
import numpy as np
import pandas as pd

#Calculate Recall and precision statistics from built forest
#Input: tagArray = forest.predict[1], testdata = pd.read_pickle() (our email dataset)
#Output: tuple[0] = recall, tuple[1] = precision
def recallPrecisionRelevant(tagArray, testData):
    #Number of emails our system said were relevant (True Positive + False Positive)
    numTagRelevant = 0
    
    numTagIrrelevant = 0
    #Number of emails that were tagged correctly (True Positive)
    numTagCorrect = 0
    #Number of emails that are actually relevant (True Positive + False Negative)
    totalRelevant = 0
    
    annotatedTestDataCount = 0
    for i in range(len(tagArray)):
        if testData["Label"].iloc[i] == '-1':
            continue
        else:
            annotatedTestDataCount += 1
        if testData["Label"].iloc[i] == '1':
            totalRelevant = totalRelevant + 1
        if tagArray[i] == '1':
            numTagRelevant = numTagRelevant + 1
            if testData["Label"].iloc[i] == '1':

                numTagCorrect = numTagCorrect + 1
        elif testData["Label"].iloc[i] == '0' and tagArray[i] == '0':
            numTagIrrelevant += 1
                    
            
    recall = numTagCorrect / totalRelevant
    precision = numTagCorrect / numTagRelevant
    accuracy = (numTagCorrect + numTagIrrelevant) / annotatedTestDataCount
    return recall, precision, accuracy
  
    
#Calculate F1 Statistic from precision and recall
#Input: precision statistic, recall statistic
#Output: f1 statistic
def f1Eval(recall, precision):
    numer = recall * precision
    denomer = precision + recall
    if denomer > 0:
        f1 = 2 * (numer / denomer)
    else:
        f1 = None
    return f1


    


#Display Statistics of system
#Input: predictOuput = forest.predict output, emails = df[pd.read_pickle(datapath)["Scenario"] == '401']
#Output: Display of statistics
def evalStats(predictOutput, emails):
    stats = recallPrecisionRelevant(predictOutput, emails)
    fOne = f1Eval(stats[0], stats[1])
#     print("Recall:" + str(stats[0] * 100) + "%")
#     print("Precision:" + str(stats[1] * 100) + "%")
#     print("Accuracy:" + str(stats[2] * 100) + "%")
#     print("F1:" + str(fOne))
    return stats[0], stats[1], stats[2], fOne
    
    
#Evaluate System
#Input: forest = forest object, emails = unpickled dataset of certain scenario, lsaMatrix = lsa matrix
#Output: Displayed Statistics
def evaluateSystem(randForest, emails, lsaMatrix):
    systemOut = randForest.predict(lsaMatrix)[1]
    evalStats(systemOut, emails)