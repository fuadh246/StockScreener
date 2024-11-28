from dash import html, dcc

def create_navbar():
    return html.Div(
        [
            html.H2("TA", style={"textAlign": "center", "color": "white"}),

            # Navigation Links
            html.Div([
                dcc.Link("Table View", href="/", style={"color": "white", "marginRight": "10px"}),
                dcc.Link("Stock Graph", href="/stock", style={"color": "white"}),
            ], style={"textAlign": "center", "marginBottom": "20px"}),

            # RSI Inputs
            html.Div([
                html.Div([html.H3("RSI", style={"color": "white", "marginRight": "10px", "fontWeight": "bold"})], style={"textAlign": "center", "marginBottom": "20px"}),
                html.Div(
                    [dcc.Input(id="min_rsi", type="number", placeholder="Min RSI", style={"width": "40%", "marginRight": "10px"}),
                dcc.Input(id="max_rsi", type="number", placeholder="Max RSI", style={"width": "40%"}),
            ], style={"display": "flex", "alignItems": "center", "marginBottom": "20px"})]),
            
            # MACD
            html.Div([
                html.Div([html.H3("MACD Signals", style={"color": "white", "marginRight": "10px", "fontWeight": "bold"})], style={"textAlign": "center", "marginBottom": "10px"}),
                dcc.Dropdown(
                    id="macd_signal",
                    options=[
                        {"label": "Bullish Crossover (Buy)", "value": "bullish_crossover"},
                        {"label": "Bearish Crossover (Sell)", "value": "bearish_crossover"},
                        {"label": "Bullish Divergence", "value": "bullish_divergence"},
                        {"label": "Bearish Divergence", "value": "bearish_divergence"},
                    ],
                    placeholder="Select MACD Signal",
                    style={"width": "100%", "margin": "0 auto", "marginBottom": "20px"},
                ),
            ]),
        ],
        
        style={
            "backgroundColor": "skyblue",
            "padding": "20px",
            "width": "250px",
            "height": "100vh",
            "position": "fixed",
            "top": "0",
            "left": "0",
        }
    )
