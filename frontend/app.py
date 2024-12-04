import dash
from dash import Dash, html, dcc
from components.error import display_error_message
from components.navbar import create_home_navbar,create_stock_graph_navbar 

# Initialize the Dash App
app = Dash(__name__, use_pages=True,suppress_callback_exceptions=True)
app.title = "Stock Screener App"

# Register pages
# dash.register_page("home", path="/")
# dash.register_page("stock_graph", path_template="/stock/<ticker>")
# top to are registered on their own page
dash.register_page("error", path="/error")  # Register error page

# app Layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # track current URL
    html.Div(id="navbar"),  # placeholder for navbar
    dash.page_container  # placeholder for dynamic page content
])

# callback to update navbar dynamically
@app.callback(
    dash.Output("navbar", "children"),
    dash.Input("url", "pathname")
)
def update_navbar(pathname):
    if pathname == "/":
        return create_home_navbar()
    elif pathname.startswith("/stock/"):
        return create_stock_graph_navbar()
    else:
        # Pass the pathname argument to display an error page
        return display_error_message(pathname)

# Run the App
# If you need to debug, set debug=True
if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8050)
    

# To run the app.py, Run "PYTHONPATH=$(pwd) python frontend/app.py"