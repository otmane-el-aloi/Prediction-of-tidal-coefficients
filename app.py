# External
import pandas as pd
import numpy as np
from flask import Flask, render_template, request 

# Internal
from models.RfModel import RFModel
from dataLoader.DataPredictionCreator import DataPredictionCreator

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def hello():
    if request.method == "POST":
        # Get data from the request
        from_year = int(request.form.get("from_year"))
        from_month = int(request.form.get("from_month"))
        from_day = int(request.form.get("from_day"))
        to_year = int(request.form.get("to_year"))
        to_month = int(request.form.get("to_month"))
        to_day = int(request.form.get("to_day"))

        # Create data for the model
        df, dates = DataPredictionCreator().createData(from_year, from_month, from_day, to_year, to_month, to_day)

        # Load the model
        RF = RFModel({"n_estimators":100})
        RF.load("RF_custom_features_two_target_best.pk")

        # Make prediction 
        y_predicted = RF.predict(df)

        # Getting only integer format
        y_predicted = np.array(list(map(lambda l: [int(l[0]), int(l[1])], y_predicted.tolist())))

        ziped_result = zip(dates, y_predicted)

        # Write data back to table
        return render_template("index.html", ziped_result = ziped_result)
    else :
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
