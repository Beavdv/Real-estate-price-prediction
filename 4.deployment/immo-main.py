from flask import Flask, request, render_template
from main import prediction
from flask import jsonify
import pandas as pd
import joblib

app = Flask(__name__, template_folder='template')

filename = "./finalized_model.sav"
loaded_model = joblib.load(filename)

def prediction(dict):
    df=pd.DataFrame([dict])
# load the model from disk
    predicted_price = loaded_model.predict(df)
    return predicted_price[0]

@app.route("/predict", methods=["POST"])
def predict():
    price=prediction(request.form)
    return jsonify({'price':price})

if __name__ == '__main__':
   app.run(host="127.0.0.1", port=5000, debug=True)


