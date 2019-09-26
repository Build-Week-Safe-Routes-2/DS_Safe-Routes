import json
import os
import numpy as np
import pandas as pd
import requests
from haversine import haversine, Unit
from sklearn.externals import joblib
from datetime import datetime

df_db = pd.read_csv('df_db.csv')
model = joblib.load('model.joblib')
weather_dict = {
        'Clear': 1,
        'Clouds': 10,
        'Rain': 2,
        'Thunderstorm': 2,
        'Snow': 4,
        'Sand': 7,
        'Dust': 7,
        'Smoke': 5,
        'Fog': 5,
        'Drizzle': 12
    }

day_week_dict = {
        2: 'Monday',
        3: 'Tuesday',
        4: 'Wednesday',
        5: 'Thursday',
        6: 'Friday',
        7: 'Saturday',
        1: 'Sunday'
}

hour_dict = {0: '12 AM', 1: '1 AM', 2: '2 AM', 
3: '3 AM', 4: '4 AM', 5: '5 AM', 6: '6 AM', 
7: '7 AM', 8: '8 AM', 9: '9 AM', 10: '10 AM', 
11: '11 AM', 12: '12 PM', 13: '1 PM', 14: '2 PM', 
15: '3 PM', 16: '4 PM', 17: '5 PM', 18: '6 PM', 
19: '7 PM', 20: '8 PM', 21: '9 PM', 22: '10 PM', 23: '11 PM'}

month_dict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

type_dict = {
       0: 'Not collision with motor vehicle',
       1: 'Front-to-rear',
       2: 'Front-to-front',
       6: 'Angle',
       7: 'Sideswipe, same direction',
       8: 'Sideswipe, opposite direction',
       9: 'Rear-to-side',
       10: 'Rear-to-rear',
       11: 'Other (end-swipes and others)',
       98: 'Not reported',
       99: 'Unknown'
}

def make_dataframe(input):
        column_headers = ['DAY', 'MONTH', 'YEAR', 'DAY_WEEK', 'LATITUDE', 
                        'LONGITUD', 'HOUR','WEATHER', 'ROUTE', 'TYP_INT', 'TWAY_ID']
        X = pd.DataFrame(input, columns=column_headers)
        y = model.predict(X)
        y_pred_proba = model.predict_proba(X)[:, 1].tolist()
        return y_pred_proba

def get_dict(output):
    list = [output[item] for index, item in enumerate(output)]
    dict = {"data": list}
    return dict

def get_type(coll):
    if coll in type_dict.keys():
        name = type_dict[coll]
    else:
        name = 'Unknown'
    return name

def get_month(month):
    if month in month_dict.keys():
        name = month_dict[month]
    else:
        name = 'Unknown'
    return name

def get_weekday(day):
    if day in day_week_dict.keys():
        name = day_week_dict[day]
    else:
        name = 'Unknown'
    return name

def get_hour(hour):
    if hour in hour_dict.keys():
        name = hour_dict[hour]
    else:
        name = 'Unknown'
    return name

def get_records(lat,lon):
    def filter(row, lat, lon):
        point1 = (lat, lon)
        point2 = (row['LATITUDE'], row['LONGITUD'])
        if haversine(point1, point2, unit=Unit.MILES) <= 3:
            return True
        else:
            return False
    m = df_db.apply(lambda row: filter(row, lat, lon), axis=1)
    df1 = df_db[m]
    return df1

def get_weather(lat, lon):
    URL = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&APPID=0ef5128501f7664ab39ed4005c3eca8d'
    r = requests.get(URL)
    data = r.json()
    if 'weather' not in data:
        weather = 1
        description = 'Unknown'
    else:
        description = data['weather'][0]['main']
        if description in weather_dict.keys():
            weather = weather_dict[description]
        else:
            weather = 99
    return weather, description

