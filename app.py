from xml.etree.ElementTree import QName
import flask
from flask import render_template
from scrapper import * 
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go


app = flask.Flask(__name__)
app.config["DEBUG"] = False

@app.route('/', methods=['GET'])
def home():
    return "<h1>Cryptocurrencies API</p>"

@app.route('/all/<crypto>', methods=['GET'])
def api_all(crypto):
    return get_data(crypto, 100)

@app.route('/graph/<crypto>', methods=['GET'])
def api_viz(crypto):
    data = get_data(crypto, 100)
    dates = [data[i]['Date'] for i in range(len(data))]
    open  = [data[i]['Open'] for i in range(len(data))]
    high  = [data[i]['High'] for i in range(len(data))]
    low   = [data[i]['Low'] for i in range(len(data))]
    close = [data[i]['Close'] for i in range(len(data))]

    fig = go.Figure( data=[go.Candlestick(x=dates, open=open, high=high, low=low, close=close)] )  
    
    fig.update_layout(title=crypto)
    
    graph = json.dumps(fig.show(), cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('graph.html', plot=graph)

app.run()