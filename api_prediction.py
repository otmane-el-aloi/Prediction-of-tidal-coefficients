# External
import pandas as pd
from flask import Flask, render_template, jsonify, request, url_for




app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def hello():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")