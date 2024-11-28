import sqlite3
import pandas as pd
from dash import html, Input, Output, get_app
from components.stock_table import create_stock_table
# from components.navbar import create_navbar
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
    # create_navbar(),
    html.H3(f"Stock Data of {stock_data['AsOfDate'][0]}", style={"textAlign": "center"}),
    create_stock_table(stock_data)
],style={"marginLeft": "270px", "padding": "20px" })

app = get_app()
@app.callback(
    Output("stock_table", "data"),
    [
        Input("min_rsi", "value"), Input("max_rsi", "value"),
        Input("macd_signal", "value"),
        Input("SMA10_condition", "value"),
        Input("SMA20_condition", "value"),
        Input("SMA50_condition", "value"),
        Input("SMA200_condition", "value"),
    ]
)
def filter_table(min_rsi, max_rsi, macd_signal, SMA10_condition, SMA20_condition, SMA50_condition, SMA200_condition):
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

    # MACD 
    if macd_signal == "bullish_crossover":
        filters.append("MACDline > MACDsignal")
    elif macd_signal == "bearish_crossover":
        filters.append("MACDline < MACDsignal")
    elif macd_signal == "bullish_divergence":
        filters.append("MACDline - MACDsignal > 0 AND Ticker IN (SELECT Ticker FROM EquityTechnicalIndicators WHERE Close < MACDline)")
    elif macd_signal == "bearish_divergence":
        filters.append("MACDline - MACDsignal < 0 AND Ticker IN (SELECT Ticker FROM EquityTechnicalIndicators WHERE Close > MACDline)")

    # SMA 
    sma_conditions = {
        "SMA10": SMA10_condition,
        "SMA20": SMA20_condition,
        "SMA50": SMA50_condition,
        "SMA200": SMA200_condition,
    }
    for sma, condition in sma_conditions.items():
        if condition == "above_close":
            filters.append(f"{sma} > Close")
        elif condition == "below_close":
            filters.append(f"{sma} < Close")
        elif condition and "above_SMA" in condition:
            comparison_sma = condition.split("_")[1]  
            filters.append(f"{sma} > {comparison_sma}")
        elif condition and "below_SMA" in condition:
            comparison_sma = condition.split("_")[1] 
            filters.append(f"{sma} < {comparison_sma}")

    # Append filters to query
    if filters:
        query += " AND " + " AND ".join(filters)

    # Execute the query
    conn = connect_to_db("data/sqlite/Equity.db")
    if conn:
        filtered_data = read_query_as_dataframe(conn, query=query, parameters=parameters)
        conn.close()  # Close the connection
        if "Ticker" in filtered_data.columns:
            filtered_data = filtered_data.sort_values(by="Ticker")
        if not filtered_data.empty:
            filtered_data["Ticker"] = filtered_data["Ticker"].apply(
                lambda ticker: f"[{ticker}](/stock/{ticker})"
            )
        return filtered_data.to_dict("records")
    return []