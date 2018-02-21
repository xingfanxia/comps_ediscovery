import pandas as pd
import CompsTFIDF
import email_filter
import pickle

df = pd.read_csv("./data/parsed/training.csv", dtype=str)
email_filtered = pd.DataFrame()
email_filtered = email_filter.full_filter_email(df)
print("Emails Cleaned")

scenario = pd.DataFrame(email_filtered[0::3])
scenario = scenario.reset_index(drop=True)
print("Emails Split")

vectorizer, matrix = CompsTFIDF.build_TFIDF_Matrix(scenario)
matrix = matrix.toarray()
print('TFIDF Matix built')

newDF = pd.DataFrame(data = matrix, columns = vectorizer.get_feature_names())
newDF["ID"] = pd.Series(scenario["ID"])
sortDF = pd.DataFrame(newDF.set_index("ID"))
print("DataFrame from Matrix built")
matrix = None
scenario = None
email_filtered = None
newDF = None

tfDict ={}
for key,value in sortDF.iterrows():
    innerDict = {}
    for i,v in value.items():
        if v != 0:
            innerDict[i] = v
        tfDict[key] = innerDict
sortDF = None
print("Dictionary Built")


sortDict = dict.fromkeys(tfDict.keys())
for key, values in tfDict.items():
    newValue = sorted(values,key=values.__getitem__,reverse = True)
    sortTerm = dict.fromkeys(newValue)
    for term in newValue:
        sortTerm[term] = values[term]
    sortDict[key] = sortTerm
print("Sorted ID's")

with open('SortedDict.pickle', 'wb') as handle:
    pickle.dump(sortDict, handle, protocol= pickle.HIGHEST_PROTOCOL)
