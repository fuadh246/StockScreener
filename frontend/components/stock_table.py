from dash import dash_table

def create_stock_table(data):
    # drop the "AsOfDate" column before
    if "AsOfDate" in data.columns:
        data = data.drop(columns="AsOfDate")
    # sort the data by the 'Ticker' column
    if "Ticker" in data.columns:
        data = data.sort_values(by="Ticker")
    # convert ticker to link and markdown
    data["Ticker"] = data["Ticker"].apply(lambda ticker: f"[{ticker}](/stock/{ticker})")
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
        data=data.to_dict("records"),  # Use the updated df here
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": "#2C2C2C",
            "color": '#FFFFFF',
            "fontWeight": "bold",
            "textAlign": "center",
        },
        style_data={
            "color": "black",
            "textAlign": "center",
        },
        style_cell={
            "textAlign": "center",
        },
        style_data_conditional=[
            # Alternating row colors
            {
                "if": {"row_index": "odd"},
                "backgroundColor": '#d1cecd',
            },
            {
                "if": {"row_index": "even"},
                "backgroundColor":'#bdbab9',
            },
        ],
        sort_action="native",
    )
