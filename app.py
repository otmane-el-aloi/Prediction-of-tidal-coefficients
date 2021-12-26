# External
import pandas as pd
import numpy as np
from flask import Flask, render_template, request 
from datetime import datetime

# Internal
from models.RfModel import RFModel
from dataLoader.DataPredictionCreator import DataPredictionCreator


app = Flask(__name__)
index_html = "index.html"

@app.route("/", methods = ["GET", "POST"])
def hello():
    if request.method == "POST":
        # Get data from the request
        try :
            from_date = datetime. strptime(
                        request.form['from_date'],
                        '%Y-%m-%d')
            from_year = int(from_date.year)
            from_month = int(from_date.month)
            from_day = int(from_date.day)

            to_date = datetime.strptime(
                        request.form['to_date'],
                        '%Y-%m-%d')
            to_year = int(to_date.year)
            to_month = int(to_date.month)
            to_day = int(to_date.day)
            # Create data for the model
            df, dates = DataPredictionCreator().createData(from_year, from_month, from_day, to_year, to_month, to_day)
        except:
            return render_template(index_html)

        # Load the model
        RF = RFModel({"n_estimators":100})
        RF.load("RF_custom_features_two_target_best.pk")

        # Make prediction 
        y_predicted = RF.predict(df)

        # Getting only integer format
        y_predicted = np.array(list(map(lambda l: [int(l[0]), int(l[1])], y_predicted.tolist())))

        ziped_result = zip(dates, y_predicted)

        # Write data back to table
        return render_template(index_html, ziped_result = ziped_result)
    else :
        return render_template(index_html)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


