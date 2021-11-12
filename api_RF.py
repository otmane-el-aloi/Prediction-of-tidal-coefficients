# External
import pandas as pd
from flask import Flask, render_template, jsonify, request, url_for

# Internal
from models.RfModel import RFModel



app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def hello():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    try:
        test_json = request.get_json()
        test = pd.read_json(test_json, orient='records')
        test['dateTime'] = pd.to_datetime(test['dateTime'])

        # Getting previous coefficients
        previous_coef = test["coef"].values
    
    except Exception as e:
        raise e

    # load model 
    RF = RFModel()
    RF.load("RF_model")
    model = RF.model

    # Making prediction 
    predicted_future_coef = model.predict(previous_coef)

    # Transform to json
    predicted_future_coef_df = pd.DataFrame(predicted_future_coef, columns = ["coef"])
    response = jsonify(predictions=predicted_future_coef_df.to_json(orient="records"))
    return response, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")