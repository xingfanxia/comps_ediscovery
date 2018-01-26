import flask
from flask_cors import CORS
import pandas as pd
from flask import Flask, jsonify, request
import json
import os, sys
app = Flask(__name__)
CORS(app)
root_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, root_dir)
from lib.dblib import Database
from lib import *
data = pd.read_pickle('../data/parsed/pickles/pickled_data_test.pickle')
db = Database()

email_key = data[['ID','Date', 'From', 'To', 'Subject']][:15].copy()
list_dump = email_key.to_dict(orient='records')
dict_dump = {
  "total": len(list_dump),
  "per_page": 5,
  "current_page": 1,
  "last_page": 14,
  "next_page_url": "http://localhost:5000/enron",
  # "prev_page_url": None,
  "from": 1,
  "to": 5
}
dict_dump['data'] = list_dump[:dict_dump["per_page"]]

# Todo:
# Add page turn with request parameteres
@app.route("/enron")
def enron():
    print(request.args)
    return(db.query(request.args))

app.run(port=5000, debug=True)
