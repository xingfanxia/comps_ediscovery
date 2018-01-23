import flask
from flask_cors import CORS
import pandas as pd
from flask import Flask, jsonify, request
import json
app = Flask(__name__)
CORS(app)
data = pd.read_pickle('../data/parsed/pickles/pickled_data_test.pickle')

email_key = data[['ID','Date', 'From', 'To', 'Subject']][:50].copy()
list_dump = email_key.to_dict(orient='records')
dict_dump = {
  "total": 200,
  "per_page": 15,
  "current_page": 1,
  "last_page": 14,
  "next_page_url": "http://localhost:5000/enron",
  # "prev_page_url": None,
  "from": 1,
  "to": 15
}
dict_dump['data'] = list_dump

# Todo:
# Add page turn with request parameteres
@app.route("/enron")
def enron():
    print(request.args)
    return jsonify(dict_dump)

app.run(port=5000, debug=True)
