import flask
from flask_cors import CORS
import pandas as pd
from flask import Flask, jsonify, request
import json
import os, sys
import pprint
import re
import collections
import random
import pickle
import time
import numpy
import traceback

'''
Setup, loading files
'''
app = Flask(__name__)
CORS(app)

root_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, root_dir)
from lib.dblib import Database
from lib import *
import Scenario4Gold
data = pd.read_pickle('../data/parsed/pickles/pickled_data_test.pickle')
db = Database()

scenario = '401'
saved_payload = None
saved_data = None
try:
    f = open('./testingData/saved_forest.pickle', 'rb')
    rnf = pickle.load(f)
    f.close()
except:
    rnf = None

with open('./testingData/SortedDict.pickle', 'rb') as handle:
    tfidf_dict = pickle.load(handle)

topics = pd.read_pickle('../data/parsed/LSA_dataframes/pickled_LSA_termsFeb12.pickle')
topic_dict = {}
topic_arrays = topics.values.tolist()
for i, row in enumerate(topic_arrays):
    topic_dict[i] = row

imp_data = None

'''
Methods used in pagination regexes to get last and next pages
'''
def addone(obj):
     val = int(obj.group(1))
     return str(val+1)

def subone(obj):
    val = int(obj.group(1))
    return str(val-1)

def upload_sort(search_dict, dict_tfidf, db_data):
    if ("Message_Contents" in search_dict) and (imp_data == None):
        for i in range(len(db_data)):
            if dict_tfidf[db_data[i]["ID"]].get(search_dict["Message_Contents"]) == None:
                db_data[i]["TF-IDF Value"] = 0
            else:
                db_data[i]["TF-IDF Value"] = dict_tfidf[db_data[i]["ID"]].get(search_dict["Message_Contents"])
        db_data = sorted(db_data, key=lambda k: k['TF-IDF Value'], reverse = True)
    else:
        db_data = sorted(db_data, key=lambda k: k['Relevant'], reverse=True)
    return db_data

'''
Model table data that gets populated by enron()
'''
dict_dump = {
  "total": 0,
  "per_page": 0,
  "current_page": 0,
  "last_page": 0,
  "next_page_url": "http://localhost:5000/enron",
  "prev_page_url": None,
  "from": 0,
  "to": 0
}

'''
endpoint for tree metadata for visualizations
'''
@app.route("/pred_meta/<identifier>")
def pred_data(identifier):
    if imp_data:
        data_array = []
        for key, val in imp_data[identifier].items():
            new_dict = dict()
            new_dict['topic'] = key
            new_dict['importance'] = val
            new_dict['words'] = topic_dict[int(key)]
            data_array.append(new_dict)
        response = dict()
        response['data'] = data_array
        return jsonify(response)
    else:
        return jsonify({})

@app.route("/pred_meta_color/<identifier>")
def pred_data_color(identifier):
    if imp_data:
        return jsonify(imp_data[identifier])
    else:
        return jsonify({})

'''
endpoint for topic data for visualizations
'''
@app.route("/topic_table")
def table_data_endpoint():
    topic_terms = [val for key, val in topic_dict.items()]
    topics = [key for key, val in topic_dict.items()]
    response = dict()
    response['data'] = []
    for i in range(len(topics)):
        each_topic = dict()
        each_topic['topic'] = topics[i]
        each_topic['terms'] = topic_terms[i]
        response['data'].append(each_topic)
    return flask.jsonify(response)

@app.route("/topics")
def topic_endpoint():
    return flask.jsonify(topic_dict)

@app.route("/span_data/<identifier>")
def span_data(identifier):
    word_dict = {}
    if imp_data:
        relevant_topics = imp_data[identifier]
        for key, value in relevant_topics.items():
            if key == 'Date' or key == 'To' or key == 'From':
                print('skipping date')
            else:
                for word in topic_dict[int(key)]:
                    try:
                        word_dict[word].append((value,key))
                    except KeyError:
                        word_dict[word] = [(value,key)]
        for key, value in word_dict.items():
            word_dict[key] = max(value, key=lambda item:abs(item[0]))

    return(jsonify(word_dict))


'''
reset endpoint to clear database of any user-tagged data
'''
@app.route("/reset")
def reset():
    global saved_payload
    global rnf
    try:
        db.reset_relevant()
        db.reset_new_tag()
        saved_payload = None
        rnf = None
        f = open('../saved_forest.pickle', 'wb')
        pickle.dump(rnf, f)
        f.close()
        print('reset!')
        response = {
            'status_code': 200,
            'message' : 'Reset was a success! Please reload your webpage'
        }
    except:
        print('fail')
        response = {
            'status_code': 500
        }
    return(jsonify(response))

'''
endpoint to recieve feedback (user tagged documents) and update database and table json
'''
@app.route('/feedback',methods=['GET','POST'])
def log_feedback():
    global saved_data
    feedback = request.get_json()
    print(feedback['ID'], feedback['Relevant'])
    for item in saved_data:
        if item["ID"] == feedback['ID']:
            item['Relevant'] = str(feedback['Relevant'])
    try:
        db.set_relevancy(feedback['ID'], scenario, feedback['Relevant'])
        response = {
            'status_code': 200,
            'message': "Success!\nFeedback is successfully logged to the backend database for incremental learning!"
        }
    except:
        response = {
            'status_code': 500,
            'message': "ERROR!\nFeedback is not successfully passed to the backend!"
        }
    return jsonify(response)

'''
Endpoint that recieves a query, constructs the datastructure vuetable needs to populate, and returns it
'''
@app.route("/enron")
def enron():
    global saved_data
    global saved_payload
    payload = request.args.to_dict()
    dict_dump_copy = dict(dict_dump)

    #THESE DONT WORK RIGHT YET - THE REGEX WILL PICK UP OTHER NUMBERS IN THE URL NO BUENO
    next_page = re.sub('({})'.format(payload['page']),addone,request.url)
    dict_dump_copy["next_page_url"] = next_page


    if int(payload['page']) > 1:
        prev_page = re.sub('({})'.format(payload['page']),subone,request.url)
        dict_dump_copy["prev_page_url"] = prev_page


    dict_dump_copy['sort'] = payload['sort']
    dict_dump_copy['current_page'] = payload['page']
    dict_dump_copy['per_page'] = payload['per_page']
    dict_dump_copy['from'] = 1 + int(dict_dump_copy['per_page'])*(int(dict_dump_copy['current_page']) - 1)
    del payload['sort']
    del payload['page']
    del payload['per_page']
    pprint.pprint(payload)

    if payload != saved_payload:
        data = db.query(payload)
        saved_data = data
        saved_payload = payload
    else:
        data = saved_data
    
    data = upload_sort(payload, tfidf_dict, data)


    final_len = dict_dump_copy['from'] + int(dict_dump_copy['per_page']) - 1
    if final_len > len(data):
        final_len = len(data)
    dict_dump_copy['to'] = final_len
    dict_dump_copy['data'] = data[(dict_dump_copy['from'] - 1):(dict_dump_copy['to'])]
    dict_dump_copy['total'] = len(data)
    dict_dump_copy['last_page'] = int(len(data)/int(dict_dump_copy['per_page'])) + 1
    return jsonify(dict_dump_copy)

'''
endpoint to call incremental learning which will update the predicted value of the untagged emails
'''
@app.route('/dbtest')
def dbtest():
    start = time.time()
    global imp_data
    print("Running Incremental Learning")
    global rnf
    global saved_payload
    lsa_np = np.load('../data/parsed/lsa_output.npy')
    lsa_df = pd.DataFrame(lsa_np)

    metadata = db.df_from_table('emails')
    metadata = metadata.loc[metadata['Scenario'] == scenario]
    metadata = metadata.reset_index(drop=True)

    df = pd.concat([metadata, lsa_df], axis=1, join_axes=[metadata.index])

    cat_features = ['To','From']
    features = list(range(100))
    features.extend(cat_features + ['Date'])

    df = df[features + ['Label'] + ['Relevant'] + ['ID'] + ['New_Tag']]

    print('making rnf')
    if rnf == None:
        print('there is none')
        train_df = df.loc[df['Relevant'].isin(['0','1'])]
        train_df = train_df.reset_index(drop=True)
        print (train_df.head())
        test_df = df.loc[df['Relevant'] != '1']
        test_df = df.loc[df['Relevant'] != '0']
        test_df = test_df.reset_index(drop=True)
        print (test_df.head())
        # n_trees = 32
        # tree_depth = 5
        # random_seed = 42
        # n_max_features = 11
        # n_max_input = 300
        # benchmark = None
        n_trees = 5
        tree_depth = 5
        random_seed = 42
        n_max_features = 3
        n_max_input = 300
        benchmark = None


        try:
            #train_data, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features):
            rnf = RNF(train_df, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features, user_input=True)
            rnf.fit_parallel()
            print('fit done')
            result = rnf.predict_parallel(test_df, importance=True)
            print('predict done')
            probas = result[0]
            rlvnt = [x[0] for x in probas]

            for r in rlvnt:
                if type(r) != numpy.float64:
                    print(r, type(r))

            ids = result[2]
            temp = result[3]

            if len(probas) != len(ids):
                print("not equal len!")
                exit(0)
            imp_data = dict()
            for i, identifier in enumerate(ids):
                imp_data[identifier] = temp[i]

            # data = db.df_from_table('emails', scenario=scenario)
            # for i, email in enumerate(ids):
            #     data.loc[data['ID'] == email, 'Relevant'] = probas[i]
            # db.df_to_table(data, 'emails')

            # for i, email in enumerate(ids):
            #     db.set_relevancy(email, scenario, probas[i][0])


            data = db.df_from_table('emails', scenario=scenario, time=False)
            probID = pd.DataFrame({'ID' : ids, 'Relevant' : rlvnt}).sort_values(by = ['ID']).reset_index(drop=True)
            mask = data['ID'].isin(ids)

            unchanged = pd.DataFrame(data.loc[~mask])
            change = pd.DataFrame(data.loc[mask]).sort_values(by = ['ID']).reset_index(drop=True).drop('Relevant', axis=1)
            change['Relevant'] = probID['Relevant'].values

            data = pd.concat([unchanged,change])
            #TODO: find why there are NaNs

            # print(data[data.isnull().any(axis=1)])

            # print(data[data['ID'] == '3.97882.O0BKFVNBDWGGLAN12HZZLRD0I0PW2TE2A'])
            db.df_to_table(data, 'emails')


            saved_payload = None
                # set_relevancy(self, id, scenario, score)

            # eval_dict = Scenario4Gold.scenario_4_Gold(rnf)

            response = {
                'status_code': 200,
                'message': "Success: Incremental Learning Completed!!"
            }
        except Exception as e:
            print(e)
            traceback.print_exc()
            response = {
                'status_code': 500,
                'message': "ERROR!\nIncremental training failed!"
            }
        # traceback.print_tb(e.__traceback__)
    else:
        update_df = df.loc[df['New_Tag'] == '1']
        test_df = df.loc[df['Relevant'] != '1']
        test_df = df.loc[df['Relevant'] != '0']
        test_df = test_df.reset_index(drop=True)

        try:
            rnf.update(update_df)
            result = rnf.predict_parallel(test_df, importance=True)
            probas = result[0]
            rlvnt = [x[0] for x in probas]
            ids = result[2]
            temp = result[3]
            imp_data = dict()
            for i, identifier in enumerate(ids):
                imp_data[identifier] = temp[i]

            data = db.df_from_table('emails', scenario=scenario, time=False)
            probID = pd.DataFrame({'ID' : ids, 'Relevant' : rlvnt}).sort_values(by = ['ID']).reset_index(drop=True)
            mask = data['ID'].isin(ids)

            unchanged = pd.DataFrame(data.loc[~mask])
            change = pd.DataFrame(data.loc[mask]).sort_values(by = ['ID']).reset_index(drop=True).drop('Relevant', axis=1)
            change['Relevant'] = probID['Relevant'].values

            data = pd.concat([unchanged,change])
            data['New_Tag'] = 0
            #TODO: find why there are NaNs
            db.df_to_table(data, 'emails')

            saved_payload = None

            # eval_dict = Scenario4Gold.scenario_4_Gold(rnf)

            response = {
                'status_code': 200,
                'message': "Success: Incremental Learning Completed!!"
            }
        except Exception as e:
            print(e)
            traceback.print_exc()
            response = {
                'status_code': 500,
                'message': "ERROR!\nIncremental training failed!"
            }

    end = time.time()
    f = open('../saved_forest.pickle', 'wb')
    pickle.dump(rnf, f)
    f.close()
    print("DONE")
    print(end - start)
    return jsonify(response)

app.run(port=5000, debug=True)
