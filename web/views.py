import flask
from flask import Flask
app = Flask(__name__)

def fake_data():
    emails = ['email1', 'email2', 'email3']
    data = {'data' : {'emails' : emails}}
    return data

@app.route("/fakedata")
def fake_data_endpoint():
    return flask.jsonify(fake_data())

@app.route("/POC")
def poc():
    documents = fake_data()
    return flask.render_template('documentview.html', docs = documents)


app.run(debug=True)
