import sqlite3
import pandas as pd
from dash import html, dcc, Input, Output, get_app
import plotly.graph_objects as go
from dash import register_page
from backend.database import connect_to_db, read_query_as_dataframe
from components.navbar import create_navbar
from datetime import datetime, timedelta


register_page(__name__, path_template="/stock/<ticker>")
DB_PATH = "data/sqlite/Equity.db"

def connect_to_db(path):
    try:
        connection = sqlite3.connect(path)
        print(f"Connected to SQLite database at {path}")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_TA(ticker):
    conn = connect_to_db(DB_PATH)
    query = '''
        SELECT AsOfDate, Ticker, Close, Volume, SMA10, SMA20, SMA50,SMA200, RSI, MACDline, MACDsignal
        FROM EquityTechnicalIndicators
        WHERE Ticker = ?
        ORDER BY AsOfDate ASC;
    '''
    stock_data_TA = read_query_as_dataframe(conn, query=query, parameters=[ticker])
    stock_data_TA['AsOfDate'] = pd.to_datetime(stock_data_TA['AsOfDate'])
    conn.close()
    return stock_data_TA

def stock_details_page(ticker):
    conn = connect_to_db(DB_PATH)
    query = '''
        SELECT AsOfDate, Open, High, Low, Close
        FROM EquityDailyPrice
        WHERE Ticker = ?
        ORDER BY AsOfDate ASC;
    '''
    stock_data = read_query_as_dataframe(conn, query=query, parameters=[ticker])
    stock_data['AsOfDate'] = pd.to_datetime(stock_data['AsOfDate'])
    conn.close()
    
    stock_data_TA = get_TA(ticker)

    if stock_data.empty:
        return html.Div([
            create_navbar(),
            html.H3(f"No data found for ticker {ticker}", style={"textAlign": "center"}),
        ], style={"marginLeft": "270px", "padding": "20px"})

    # Generate the stock price graph
    fig = go.Figure(data=[go.Candlestick(
        x=stock_data['AsOfDate'],
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name='Candlestick'
    )])
    # Adding interactive range sliders
    fig.update_layout(
        title='Stock Candlestick Chart',
        xaxis_title='AsOfDate',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True,  # Range slider enabled
        xaxis_range=[stock_data['AsOfDate'].min(), stock_data['AsOfDate'].max()],  # Default to full range
    )
    

    # page layout
    return html.Div([
        create_navbar(),
        html.H3(f"Stock Details for {ticker}", style={"textAlign": "center"}),
        dcc.Graph(figure=fig)
    ], style={"marginLeft": "270px", "padding": "20px"})


layout = html.Div([
    dcc.Location(id="url"),  # Add the URL component
    html.Div(id="stock-details-content")
])

# Callback to dynamically update the page content
app = get_app()

@app.callback(
    Output("stock-details-content", "children"),
    Input("url", "pathname")  # Listen to changes in the URL
)
def update_stock_page(pathname):
    """
    Update the stock details page based on the ticker from the URL.
    """
    if not pathname:
        return html.Div("No stock selected.", style={"textAlign": "center", "padding": "20px"})
    
    ticker = pathname.split("/")[-1]  # Extract the ticker from the URL
    return stock_details_page(ticker)
