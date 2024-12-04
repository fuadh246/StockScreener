from dash import html

def display_error_message(pathname):
        return html.Div([
            html.H1("⚠️ Error: Missing Ticker", style={"color": "red", "textAlign": "center"}),
            html.P(
                "It seems like you navigated to an unknown page without providing a ticker.",
                style={"textAlign": "center", "fontSize": "18px"}
            ),
            html.P(
                "Please provide a ticker after '/stock/' in the URL, like '/stock/AAPL'.",
                style={"textAlign": "center", "fontSize": "16px"}
            ),
            html.A(
                "🏠 Go Back to Homepage",
                href="/",
                style={
                    "display": "block",
                    "textAlign": "center",
                    "marginTop": "20px",
                    "color": "blue",
                    "fontSize": "18px",
                    "textDecoration": "underline",
                }
            )
        ], style={
            "border": "2px solid red",
            "borderRadius": "10px",
            "padding": "20px",
            "margin": "50px auto",
            "width": "60%",
            "backgroundColor": "#ffe6e6"
        })