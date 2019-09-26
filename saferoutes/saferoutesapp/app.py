from flask import Flask, render_template, jsonify, request
import json
import os
from .util import *
import numpy as np
import pandas as pd
import requests
from flask_cors import CORS, cross_origin
from datetime import datetime

today = datetime.today()

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    @app.route('/index')
    @app.route('/api', methods=['POST'])
    def prediction():
        input = request.get_json(force=True)
        data = []
        records = get_records(input['LATITUDE'], input['LONGITUD'])
        output = {}
        for i in range(len(records)):
            weather = get_weather(input['LATITUDE'], input['LONGITUD'])
            observation = [today.day, today.month, today.year, 
                            today.weekday(), records['LATITUDE'].values[i], 
                            records['LONGITUD'].values[i], today.hour, 
                            weather[0], records['ROUTE'].values[i], 
                            records['TYP_INT'].values[i], records['TWAY_ID'].values[i]]
            data.append(observation)
            result = make_dataframe(data)
            if result[i] < 0.2:
                message = 'Low'
            else:
                message = 'Moderate to High'

            output[i] = {
            "latitude": records['LATITUDE'].values[i],
            "longitude": records['LONGITUD'].values[i],
            "current_weather": weather[1],
            "probability_accident": str(round(result[i]*100, 2))+'%',
            "risk_level": message,
            "accidents_2015": int(records.groupby(['YEAR'])['STATE'].agg('count').values[0]),
            "accidents_2016": int(records.groupby(['YEAR'])['STATE'].agg('count').values[1]),
            "accidents_2017": int(records.groupby(['YEAR'])['STATE'].agg('count').values[2]),
            "fatalities_2015": int(records.groupby(['YEAR'])['FATALS'].sum().values[0]),
            "fatalities_2016": int(records.groupby(['YEAR'])['FATALS'].sum().values[1]),
            "fatalities_2017": int(records.groupby(['YEAR'])['FATALS'].sum().values[2]),
            "weekday_most_accidents": get_weekday(records['DAY_WEEK'].value_counts().idxmax()),
            "month_most_accidents": get_month(records['MONTH'].value_counts().idxmax()),
            "hour_most_accidents": get_hour(records['HOUR'].value_counts().idxmax()),
            "most_common_type_collision": get_type(records['MAN_COLL'].value_counts().idxmax())
            }

        result = get_dict(output)
        return result

    return app