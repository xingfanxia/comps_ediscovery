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

saved_payload = None
saved_data = None

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

# Todo:
# Add page turn with request parameteres
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

app.run(port=5000, debug=True)
