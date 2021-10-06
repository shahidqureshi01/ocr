from flask import Flask, request, jsonify, render_template, url_for
from flask import Flask, render_template, session, copy_current_request_context
from threading import Lock
import sklearn
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/',methods = ['POST'])
def predict():
  return render_template('index.html', prediction_text="Newton Predicts {}".format(prediction[0]))


if __name__ == '__main__':
    app.run(debug=True)