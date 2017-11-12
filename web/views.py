import flask
import pandas as pd
from flask import Flask
import json
app = Flask(__name__)

data = pd.read_pickle('../data/parsed/pickles/pickled_data_test.pickle')

email_key = data[['Date', 'From', 'To', 'Subject']][:500].copy()
email_key_dict = email_key.to_dict(orient='index')

def fake_data():
    emails = ['email1', 'email2', 'email3']
    data = {
  'items': [
    { 'Sender' : 'John Doe', 'Receiver' : 'Jill Doe', 'Subject' : 'Pizza Tonight?', 'Sent_Date' : '1/1/17', 'Contents' : "Yo", 'id' : 0 },
    { 'Sender': 'Bob Doe', 'Receiver' : 'John Doe', 'Subject' : 'Pasta Tonight?', 'Sent_Date' : '2/1/17', 'Contents' : "hell0", 'id' : 1 },
    { 'Sender': 'Elliot Doe', 'Receiver' : 'Randy Doe', 'Subject' : '\'za Tonight?', 'Sent_Date' : '3/1/17', 'Contents' : "whats up", 'id' : 2 },
    { 'Sender': 'John Doe', 'Receiver' : 'Jill Doe', 'Subject' : 'Yolo', 'Sent_Date' : '4/1/17', 'Contents' : "butts", 'id' : 3 }
  ]
}
    return data

@app.route("/fakedata")
def fake_data_endpoint():
    return flask.jsonify(fake_data())

@app.route("/datakey")
def data_key_endpoint():
    return flask.jsonify(email_key_dict)

@app.route("/data/<int:id>")
def data_endpoint(id):
    row = data.loc[id].to_dict()
    print(row)
    return flask.jsonify(row)

@app.route("/POC")
def poc():
    documents = fake_data()
    return flask.render_template('documentview.html', docs = documents)


app.run(debug=True)
adsf
