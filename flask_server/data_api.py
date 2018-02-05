import flask
from flask_cors import CORS
import pandas as pd
from flask import Flask, jsonify, request
import json
import os, sys
import pprint
import re

app = Flask(__name__)
CORS(app)

root_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, root_dir)
from lib.dblib import Database
from lib import *
data = pd.read_pickle('../data/parsed/pickles/pickled_data_test.pickle')
db = Database()

scenario = '401'
saved_payload = None
saved_data = None
rnf = None

def addone(obj):
     val = int(obj.group(1))
     return str(val+1)

def subone(obj):
    val = int(obj.group(1))
    return str(val-1)

email_key = data[['ID','Date', 'From', 'To', 'Subject']][:15].copy()
list_dump = email_key.to_dict(orient='records')
dict_dump = {
  "total": len(list_dump),
  "per_page": 5,
  "current_page": 1,
  "last_page": 14,
  "next_page_url": "http://localhost:5000/enron",
  "prev_page_url": None,
  "from": 1,
  "to": 5
}

@app.route('/feedback',methods=['GET','POST'])
def log_feedback():
    feedback = request.get_json()
    print(feedback['ID'], feedback['Relevant'])
    db.set_relevancy(feedback['ID'], scenario, feedback['Relevant'])
    return '{"status": 200}\n'

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

    final_len = dict_dump_copy['from'] + int(dict_dump_copy['per_page']) - 1
    if final_len > len(data):
        final_len = len(data)
    dict_dump_copy['to'] = final_len
    dict_dump_copy['data'] = data[(dict_dump_copy['from'] - 1):(dict_dump_copy['to'])]
    dict_dump_copy['total'] = len(data)
    dict_dump_copy['last_page'] = int(len(data)/int(dict_dump_copy['per_page'])) + 1
    return jsonify(dict_dump_copy)

@app.route('/dbtest')
def dbtest():
    print("Running Incremental Learning")
    global rnf
    lsa_np = np.load('../data/parsed/lsa_output.npy')
    lsa_df = pd.DataFrame(lsa_np)

    metadata = db.df_from_table('emails')
    metadata = metadata.loc[metadata['Scenario'] == '401']
    metadata = metadata.reset_index(drop=True)

    df = pd.concat([metadata, lsa_df], axis=1, join_axes=[metadata.index])

    cat_features = ['To','From']
    features = list(range(100))
    features.extend(cat_features + ['Date'])

    df = df[features + ['Label'] + ['Relevant'] + ['ID']]

    if rnf == None:
        train_df = df.loc[df['Relevant'] != '-1']
        train_df = train_df.reset_index(drop=True)
        print (train_df.head())
        test_df = df.loc[df['Relevant'] == '-1'][:100]
        test_df = test_df.reset_index(drop=True)
        print (test_df.head())
        n_trees = 64
        tree_depth = 5
        random_seed = 42
        n_max_features = 11
        n_max_input = 300
        benchmark = None

        #train_data, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features):
        rnf = RNF(train_df, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features, user_input=True)
        rnf.fit_parallel()
        print(rnf.predict(test_df))
    return '{"status": 200}\n'

app.run(port=5000, debug=True)
