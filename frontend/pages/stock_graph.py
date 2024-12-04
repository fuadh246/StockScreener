import sqlite3
import pandas as pd
from dash import register_page
import plotly.graph_objects as go
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
from dash import html, dcc, Input, Output, get_app
from backend.database import connect_to_db, read_query_as_dataframe

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
            # create_navbar(),
            html.H3(f"No data found for ticker {ticker}", style={"textAlign": "center"}),
        ], style={"marginLeft": "270px", "padding": "20px"})

    stock_data['RSI'] = stock_data_TA['RSI']
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True, 
        vertical_spacing=0.2, 
        row_heights=[2, 1, 1],
    )

    # add candlestick chart
    fig.add_trace(go.Candlestick(
        x=stock_data['AsOfDate'],
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name='Candlestick',
        hoverinfo="x+y"
    ), row=1, col=1)

    # add SMA
    sma_columns = ['SMA10', 'SMA20', 'SMA50', 'SMA200']
    sma_colors = {'SMA10': 'blue', 'SMA20': 'orange', 'SMA50': 'green', 'SMA200': 'red'}

    for sma in sma_columns:
        if sma in stock_data_TA: 
            fig.add_trace(go.Scatter(
                x=stock_data['AsOfDate'],
                y=stock_data_TA[sma],
                mode='lines',
                name=sma,
                line=dict(color=sma_colors[sma], width=1.5)
            ), row=1, col=1)

    # add RSI line chart with threshold
    fig.add_trace(go.Scatter(
        x=stock_data['AsOfDate'],
        y=stock_data['RSI'],
        mode='lines',
        name='RSI',
        line=dict(color='blue')
    ), row=2, col=1)

    # add RSI thresholds
    fig.add_trace(go.Scatter(
        x=stock_data['AsOfDate'],
        y=[70] * len(stock_data),
        mode='lines',
        name='Overbought (70)',
        line=dict(color='red', dash='dot'),
        showlegend=True
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=stock_data['AsOfDate'],
        y=[30] * len(stock_data),
        mode='lines',
        name='Oversold (30)',
        line=dict(color='green', dash='dot'),
        showlegend=True
    ), row=2, col=1)

    # MACD 
    fig.add_trace(go.Scatter(
        x=stock_data['AsOfDate'],
        y=stock_data_TA['MACDline'],
        mode='lines',
        name='MACDline',
        line=dict(color='green'),
        showlegend=True
    ), row=3, col=1)
    fig.add_trace(go.Scatter(
        x=stock_data['AsOfDate'],
        y=stock_data_TA['MACDsignal'],
        mode='lines',
        name='MACDsignal',
        line=dict(color='red',),
        showlegend=True
    ), row=3, col=1)

    fig.update_layout(
        autosize=True,  
        height=None,   
        width=None,    
        yaxis_title='Price',
        yaxis2_title='RSI',
        yaxis3_title='MACD',
        xaxis3_title='Date', 
        xaxis_rangeslider_visible=True,
        xaxis_range=[stock_data['AsOfDate'].min(), stock_data['AsOfDate'].max()],
        hovermode="x unified", 
        font=dict(size=14), 
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # page layout
    return html.Div([
        html.H3(f"Stock Details for {ticker}", style={"textAlign": "center"}),
        dcc.Graph(
            id="stock-graph",
            figure=fig,
            style={"width": "100%", "height": "calc(100vh - 50px)"}  
        )
    ], style={"marginLeft": "270px", "padding": "20px"})


layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="stock-details-content")
])


app = get_app()

@app.callback(
    Output("stock-details-content", "children"),
    Input("url", "pathname")  # listen to changes in the URL
)
def update_stock_page(pathname):
    """
    Update the stock details page based on the ticker from the URL.
    """
    if not pathname:
        return html.Div("No stock selected.", style={"textAlign": "center", "padding": "20px"})
    
    ticker = pathname.split("/")[-1] # gets the ticker
    return stock_details_page(ticker)

