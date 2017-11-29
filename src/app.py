import pickle
import os
from flask import Flask, jsonify, request

clf_loc = os.getenv('CLFPATH')
vect_loc = os.getenv('VECTPATH')
with open(clf_loc, 'rb') as f:
    clf = pickle.load(f)
with open(vect_loc, 'rb') as f:
    vect = pickle.load(f)

app = Flask(__name__)

@app.route('/score')
def score():
    title = request.args.get('title')
    title_ct = vect.transform([title])

    proba = clf.predict_proba(title_ct)[0][1]
    classification = bool(clf.predict(title_ct)[0] > 0.5)

    return jsonify({'score': proba, 'clf': classification})

with open('index.html', 'r') as f:
    index_html = f.read()

@app.route('/')
def index():
    return index_html

if __name__ == '__main__':
    app.run(debug=True)
