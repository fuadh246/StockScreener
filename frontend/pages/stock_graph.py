from dash import html, dcc, Input, Output, get_app
import plotly.express as px
import pandas as pd
import numpy as np

import pandas as pd

stock_data = pd.DataFrame({
    "Stock": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
    "Price": [150.25, 320.15, 2805.67, 3450.50, 720.88],
    "Volume": [100000, 150000, 120000, 80000, 90000],
    "RSI": [45, 55, 62, 40, 48]
})

# Register the page
from dash import register_page
register_page(__name__, path="/graph")

# Page Layout
layout = html.Div([
    html.H3("Stock Graph", style={"textAlign": "center"}),

    # Dropdown for selecting stock
    html.Div([
        dcc.Dropdown(
            id="stock_dropdown",
            options=[{"label": stock, "value": stock} for stock in stock_data["Stock"]],
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

    # Dummy time-series data for the stock
    dates = pd.date_range(start="2023-01-01", periods=100)
    base_prices = 150 + 20 * np.sin(2 * np.pi * dates.day_of_year / 365)  # Base prices using sine wave
    random_adjustments = np.random.uniform(-5, 5, size=100)  # Random adjustments between -5 and 5
    prices = base_prices + random_adjustments  # Adjust prices randomly


    # Create DataFrame
    df = pd.DataFrame({"Date": dates, "Price": prices}).reset_index(drop=True)
    df["Stock"] = selected_stock

    # Create graph
    return px.line(df, x="Date", y="Price", title=f"{selected_stock} Price Over Time")
