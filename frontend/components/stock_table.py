from dash import dash_table

def create_stock_table(data):
    # Drop the "AsOfDate" column before passing data to the DataTable
    if "AsOfDate" in data.columns:
        data = data.drop(columns="AsOfDate")
    
    # Sort the data by the 'Ticker' column
    if "Ticker" in data.columns:
        data = data.sort_values(by="Ticker")
    
    
    # covert to link
    data["Ticker"] = data["Ticker"].apply(lambda ticker : f"[{ticker}](/stock/{ticker})")
    
    
    return dash_table.DataTable(
        id="stock_table",
        columns=[
            {
                "name": col,
                "id": col,
                "presentation": "markdown" if col == "Ticker" else None,
            }
            for col in data.columns
        ],
        data=data.to_dict("records"),  # Use the updated DataFrame here
        style_table={"overflowX": "auto", "padding": "10px"},
        style_header={
            "backgroundColor": "linear-gradient(to right, rgb(30, 30, 30), rgb(60, 60, 60))",
            "color": "black",
            "fontWeight": "bold",
            "textAlign": "center",
        },
        style_data={
            "backgroundColor": "linear-gradient(to right, rgb(50, 50, 50), rgb(70, 70, 70))",
            "color": "black",
            "textAlign": "center",
        },
        style_cell={
            "textAlign": "center",
            "border": "1px solid rgb(80, 80, 80)",  # Adds borders for better contrast
        },
        style_data_conditional=[
            {
                "if": {
                    "filter_query": "{RSI} <= 30",  # RSI is very low
                    "column_id": "RSI",
                },
                "backgroundColor": "rgba(0, 255, 0, 0.6)",  # Semi-transparent green
                "color": "black",
            },
            {
                "if": {
                    "filter_query": "{RSI} > 30 && {RSI} <= 50",  # RSI is mid-low
                    "column_id": "RSI",
                },
                "backgroundColor": "rgba(173, 255, 47, 0.6)",  # Light green/yellow
                "color": "black",
            },
            {
                "if": {
                    "filter_query": "{RSI} > 50 && {RSI} <= 70",  # RSI is mid-high
                    "column_id": "RSI",
                },
                "backgroundColor": "rgba(255, 165, 0, 0.6)",  # Orange
                "color": "black",
            },
            {
                "if": {
                    "filter_query": "{RSI} > 70",  # RSI is high
                    "column_id": "RSI",
                },
                "backgroundColor": "rgba(255, 0, 0, 0.6)",  # Semi-transparent red
                "color": "white",
            },
        ],
        sort_action="native",  # Enable sorting
    )
