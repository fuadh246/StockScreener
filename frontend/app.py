from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Screener"),
    html.P("This app allows you to screen stocks with various filters.")
])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)