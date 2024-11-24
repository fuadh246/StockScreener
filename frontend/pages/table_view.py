import sqlite3
import pandas as pd
from dash import html, Input, Output, get_app
from components.stock_table import create_stock_table
from components.navbar import create_navbar
from backend.database import connect_to_db, read_query_as_dataframe
from dash import register_page
register_page(__name__, path="/")
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
    create_navbar(),
    html.H3(f"Stock Data of {stock_data['AsOfDate'][0]}", style={"textAlign": "center"}),
    create_stock_table(stock_data)
],style={"marginLeft": "270px", "padding": "20px"})

# Use get_app() to fetch the app context
app = get_app()
@app.callback(
    Output("stock_table", "data"),
    [Input("min_rsi", "value"), Input("max_rsi", "value")]
)
def filter_table(min_rsi, max_rsi):
    # SQL query with filtering conditions
    query = '''
    SELECT AsOfDate, Ticker, Close, Volume, SMA10, SMA20, SMA50, SMA200, RSI, MACDline, MACDsignal
    FROM EquityTechnicalIndicators
    WHERE AsOfDate = (SELECT MAX(AsOfDate) FROM EquityTechnicalIndicators)
    '''
    filters = []
    parameters = []
    
    # RSI
    if min_rsi is not None:
        filters.append("RSI >= ?")
        parameters.append(min_rsi)
        
    if max_rsi is not None:
        filters.append("RSI <= ?")
        parameters.append(max_rsi)
    
    if filters:
        query += " AND " + " AND ".join(filters)



    # Execute the query
    conn = connect_to_db("data/sqlite/Equity.db")
    if conn:
        filtered_data = read_query_as_dataframe(conn, query=query, parameters=parameters)
        conn.close()  # Close the connection
        if "Ticker" in filtered_data.columns:
            filtered_data = filtered_data.sort_values(by="Ticker")
        return filtered_data.to_dict("records")
    return []