from dash import html, dcc

def create_sma_filter(sma_values):
    """Generate SMA filtering dropdowns dynamically with multiple comparison options."""
    sma_dropdowns = []
    for sma in sma_values:
        options = [
            {"label": "Above Close Price", "value": "above_close"},
            {"label": "Below Close Price", "value": "below_close"},
        ]
        # add options with other
        for compare_sma in sma_values:
             # ignore comparing with itself
            if sma != compare_sma: 
                options.append({"label": f"Above SMA{compare_sma}", "value": f"above_SMA{compare_sma}"})
                options.append({"label": f"Below SMA{compare_sma}", "value": f"below_SMA{compare_sma}"})

        sma_dropdowns.append(
            html.Div([
                html.Div(
                    [html.H3(f"SMA{sma}", style={"color": "white", "fontWeight": "bold"})],
                    style={"textAlign": "center", "marginBottom": "10px"}
                ),
                dcc.Dropdown(
                    id=f"SMA{sma}_condition",
                    options=options,
                    placeholder=f"Select condition for SMA{sma}",
                    style={"width": "100%", "marginBottom": "20px"},
                ),
            ])
        )
    return sma_dropdowns

def create_navbar():
    sma_values =[10,20,50,200]
    return html.Div(
        [
            html.H2("TA", style={"textAlign": "center", "color": "white"}),

            # Navigation Links
            html.Div([
                dcc.Link("Table View", href="/", style={"color": "white", "marginRight": "10px"}),
                # dcc.Link("Stock Graph", href="/stock", style={"color": "white"}),
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
            *create_sma_filter(sma_values)
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
