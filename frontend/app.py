from dash import Dash, html
import dash

from components.navbar import create_navbar  # Import Navbar

# Initialize the Dash App
app = Dash(__name__, use_pages=True)
app.title = "Stock Screener App"

# App Layout
app.layout = html.Div([
    html.Div(
        [
            dash.page_container  # Placeholder for dynamic page content
        ],
    )
])

# Run the App
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
    
    
    
    
    
# PYTHONPATH=$(pwd) python frontend/app.py
