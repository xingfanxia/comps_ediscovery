import pandas as pd
import CompsTFIDF
import email_filter

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
matrix = None
scenario = None
email_filtered = None
newDF = None
tfDict = sortDF.to_dict('index')
sortDF = None
print("Full Dictionary Built")

for key, values in list(tfDict.items()):
    for term,freq in list(values.items()):
        if freq == 0:
            values.pop(term,freq)
print("Zero's removed")

sortDict = dict.fromkeys(tfDict.keys())
for key, values in tfDict.items():
    newValue = sorted(values,key=values.__getitem__,reverse = True)
    sortTerm = dict.fromkeys(newValue)
    for term in newValue:
        sortTerm[term] = values[term]
    sortDict[key] = sortTerm
print(sortDict)
print("Sorted ID's")

with open('SortedDict.pickle', 'wb') as handle:
    pickle.dump(sortDict, handle, protocol= pickle.HIGHEST_PROTOCOL)
