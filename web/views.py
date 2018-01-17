
import flask
import pandas as pd
from flask import Flask, request
import json
app = Flask(__name__)
import os, sys
root_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, root_dir)
from lib.dblib import Database
from lib import *

#Global Vars
scenario = '401'
db = Database()
email_list = db.get_scenario(scenario)
rnf = None

# data = pd.read_pickle('../data/parsed/pickles/pickled_data_test.pickle')
# data['Relevant'] = '0'
#
# email_key = data[['ID','Date', 'From', 'To', 'Subject', 'Scenario']][:5000].copy()
# email_key_dict = email_key.to_dict(orient='index')
#
# #If there's a fast way to remove ID from v, we should do that here as well
# email_key_dict = {v['ID']:v for k, v in email_key_dict.items()}

def fake_data():
    data = {
        1 : ['the', 'but'],
        2 : ['a'],
        3 : ['for'],
        4 : ['this']
    }
    return data

@app.route("/topics")
def fake_data_endpoint():
    return flask.jsonify(fake_data())

@app.route("/datakey")
def data_key_endpoint():
    return flask.jsonify(email_list)

# @app.route("/data/<int:id>")
@app.route("/data/<id>")
def data_endpoint(id):
    # row = data.loc[id].to_dict()
    row = db.get_email_by_id(id, scenario=scenario)
    print(row)
    return flask.jsonify(row)

@app.route("/POC")
def poc():
    documents = fake_data()
    return flask.render_template('documentview.html', docs = documents)

@app.route('/feedback',methods=['GET','POST'])
def log_feedback():
    feedback = request.get_json()
    db.set_relevancy(feedback['ID'], scenario, feedback['Relevant'])
    return '{"status": 200}\n'

@app.route('/dbtest')
def dbtest():
    print("THIS IS GETTING CALLED WTF")
    global rnf
    lsa_np = np.load('../data/parsed/lsa_output.npy')
    lsa_df = pd.DataFrame(lsa_np)

    metadata = db.df_from_table('emails')
    metadata = metadata.loc[metadata['Scenario'] == 401]
    metadata = metadata.reset_index(drop=True)

    df = pd.concat([metadata, lsa_df], axis=1, join_axes=[metadata.index])

    cat_features = ['To','From']
    features = list(range(100))
    features.extend(cat_features + ['Date'])

    df = df[features + ['Label'] + ['Relevant'] + ['ID']]

    if rnf == None:
        train_df = df.loc[df['Relevant'] != -1]
        train_df = train_df.reset_index(drop=True)
        print (train_df.head())
        test_df = df.loc[df['Relevant'] == -1][:100]
        test_df = test_df.reset_index(drop=True)
        print (test_df.head())
        n_trees = 64
        tree_depth = 5
        random_seed = 42
        n_max_features = 11
        n_max_input = 300
        benchmark = None

        #train_data, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features):
        rnf = RNF(train_df, n_trees, tree_depth, random_seed, n_max_features, n_max_input, cat_features)
        rnf.fit()
        print(rnf.predict(test_df))
    return '{"status": 200}\n'



app.run(debug=True)
