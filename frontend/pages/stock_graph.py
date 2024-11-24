from dash import html, dcc, Input, Output, get_app
import plotly.express as px
import pandas as pd
import numpy as np
import sqlite3
import pandas as pd
import plotly.graph_objects as go
# Register the page
from dash import register_page
from backend.database import connect_to_db, read_query_as_dataframe
register_page(__name__, path="/graph")
DB_PATH = "data/sqlite/Equity.db"

# Get data from sqlite
# connect to database
def connect_to_db(path):
    try:
        connection = sqlite3.connect(path)
        print(f"Connected to SQLite database at {path}")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")


def get_initial_data():
    conn = connect_to_db(DB_PATH)
    query = '''
        SELECT AsOfDate, Ticker, Close, Volume, SMA10, SMA20, SMA50,SMA200, RSI, MACDline, MACDsignal
        FROM EquityTechnicalIndicators
        WHERE AsOfDate = (SELECT MAX(AsOfDate) FROM EquityTechnicalIndicators);
    '''
    stock_data = read_query_as_dataframe(conn,query)
    return stock_data

stock_data = get_initial_data()

# Page Layout
layout = html.Div([
    html.H3("Stock Graph", style={"textAlign": "center"}),

    # Dropdown for selecting stock
    html.Div([
        dcc.Dropdown(
            id="stock_dropdown",
            options=[{"label": stock, "value": stock} for stock in stock_data["Ticker"]],
            placeholder="Select a Stock",
            style={"width": "50%"}
        )
    ], style={"textAlign": "center", "marginBottom": "20px"}),

    # Graph placeholder
    dcc.Graph(id="stock_graph")
])

# Use get_app() to fetch the app context
app = get_app()

@app.callback(
    Output("stock_graph", "figure"),
    Input("stock_dropdown", "value")
)
def update_stock_graph(selected_stock):
    if not selected_stock:
        return {}

    conn = connect_to_db(DB_PATH)
    
    # Parameterized query to avoid SQL injection
    query = '''
        SELECT AsOfDate, Ticker, Close, Volume, SMA10, SMA20, SMA50, SMA200, RSI, MACDline, MACDsignal
        FROM EquityTechnicalIndicators
        WHERE Ticker = ?;
    '''
    
    data = pd.read_sql_query(query, conn, params=[selected_stock])
    conn.close()

    # Create the figure (using Plotly or another visualization library)
    fig = px.line(
        data,
        x="AsOfDate",
        y="Close",
        title=f"Stock Data for {selected_stock}",
        labels={"AsOfDate": "Date", "Close": "Closing Price"}
    )
    
    # Optionally add other traces for SMA10, SMA20, RSI, etc.
    fig.add_trace(go.Scatter(x=data["AsOfDate"], y=data["SMA10"], mode='lines', name="SMA10"))
    fig.add_trace(go.Scatter(x=data["AsOfDate"], y=data["SMA20"], mode='lines', name="SMA20"))

    return fig