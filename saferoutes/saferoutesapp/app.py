from flask import Flask, jsonify, request
import json
import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from sklearn.externals import joblib
from datetime import datetime

model = joblib.load('model.joblib')
today = datetime.today()

def create_app():
    app = Flask(__name__)
    CORS(app)

    def make_dataframe(input):
        column_headers = ['DAY', 'MONTH', 'YEAR', 'DAY_WEEK', 'LATITUDE', 
                        'LONGITUD', 'HOUR','WEATHER', 'ROUTE', 'TYP_INT', 'TWAY_ID']
        X = pd.DataFrame(input, columns=column_headers)
        y = model.predict(X)
        y_pred_proba = model.predict_proba(X)[:, 1].tolist()
        return y_pred_proba

    @app.route('/')
    @app.route('/index')
    @app.route('/api', methods=['POST'])
    def prediction():
        input = request.get_json(force=True)
        data = []
        pred = {}
        for i in range(len(input)):
            for keys, values in input[i].items():
                observation = [today.day, today.month, today.year, 
                              today.weekday(), input[i]['LATITUDE'], 
                              input[i]['LONGITUD'], input[i]['HOUR'], 
                              input[i]['WEATHER'], input[i]['ROUTE'], 
                              input[i]['TYP_INT'], input[i]['TWAY_ID']]
            data.append(observation)
            result = make_dataframe(data)
            if result[i] < 0.2:
                message = 'Low'
            else:
                message = 'Moderate to High'
            pred[i] = {
            "LATITUDE": input[i]['LATITUDE'],
            "LONGITUD": input[i]['LONGITUD'],
            "PROBABILITY OF ACCIDENT": str(round(result[i]*100, 2))+'%',
            "RISK LEVEL": message
            }
        return pred


    return app