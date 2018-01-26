import flask
from flask_cors import CORS
import pandas as pd
from flask import Flask, jsonify, request
import json
import os, sys
import pprint

app = Flask(__name__)
CORS(app)

root_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, root_dir)
from lib.dblib import Database
from lib import *
data = pd.read_pickle('../data/parsed/pickles/pickled_data_test.pickle')
db = Database()



# Todo:
# Add page turn with request parameteres
@app.route("/enron")
def enron():
    dict_dump = {
      "per_page": 5,
      "current_page": 1,
      "last_page": 14,
      "next_page_url": "http://localhost:5000/enron",
      # "prev_page_url": None,
      "from": 1,
      "to": 5
    }
    payload = request.args.to_dict()
    if_sort = payload['sort']
    page_num = payload['page']
    entries_per_page = payload['per_page']
    del payload['sort']
    del payload['page']
    del payload['per_page']
    pprint.pprint(payload)
    data = db.query(payload)
    dict_dump['data'] = data
    dict_dump['total'] = len(data)
    return jsonify(dict_dump)

app.run(port=5000, debug=True)
