from flask import Flask, render_template

# import pandas to read in CSV files
import pandas as pd

# import matplotlib + seaborn for exploratory data analysis
import plotly.graph_objects as go

APP = Flask(__name__)

@APP.route("/")
def graph():
    
    return render_template('top100.html')