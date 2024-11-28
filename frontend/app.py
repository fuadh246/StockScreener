from dash import Dash, html, dcc
import dash

from components.navbar import create_home_navbar,create_stock_graph_navbar  # Import Navbar

# Initialize the Dash App
app = Dash(__name__, use_pages=True,suppress_callback_exceptions=True)
app.title = "Stock Screener App"

# App Layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # Track current URL
    html.Div(id="navbar"),  # Placeholder for navbar
    dash.page_container  # Placeholder for dynamic page content
])

# Callback to update navbar dynamically
@app.callback(
    dash.Output("navbar", "children"),
    dash.Input("url", "pathname")
)
def update_navbar(pathname):
    if pathname == "/":
        return create_home_navbar()
    else:
        return create_stock_graph_navbar()

# Run the App
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)

    
    
# PYTHONPATH=$(pwd) python frontend/app.py
