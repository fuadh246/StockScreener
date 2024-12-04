# Stock Screener App

The Stock Screener App is an interactive, web-based stock screening tool built with Dash. It provides users with powerful filtering, analysis, and visualization features to screen stocks effectively and make data-driven decisions.

# Features

- **Stock Filtering**: Filter stocks based on parameters such as SAM, RSI, and more.

- **Interactive Dashboards**: Explore and analyze data through dynamic charts and graphs.

# Technologies Used

- **Dash**: For creating interactive web applications.

- **Plotly**: For rich data visualization and charting.

- **Pandas**: For data manipulation and analysis.

- **APIs**: Integration with financial APIs (e.g., Yahoo Finance) for fetching stock data.

- **Sqlite3**: For data storage

# Installation

To set up the project locally, follow these steps:

1. Clone the Repository:

   ```bash
   git clone https://github.com/fuadh246/StockScreener.git

   cd StockScreener
   ```

2. Set Up the Environment:

   - Create a virtual environment and activate it:

   ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

   - Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Application:

   ```bash
   PYTHONPATH=$(pwd) python frontend/app.py
   ```

   - Open your browser and navigate to http://127.0.0.1:8050

# File Structure

```
bash
.
├── README.md
├── backend
│   ├── __init__.py
│   ├── database.py
│   ├── loader.py
│   ├── option.py
│   ├── stock.py
│   └── utils.py
├── config
│   └── Dockerfile
├── data
│   ├── S&P500.csv
│   ├── create_equity_sqlite.sql
│   └── sqlite
│       └── Equity.db
├── docker-compose.yml
├── frontend
│   ├── app.py
│   ├── components
│   │   ├── __init__.py
│   │   ├── error.py
│   │   ├── navbar.py
│   │   └── stock_table.py
│   └── pages
│       ├── __init__.py
│       ├── stock_graph.py
│       └── table_view.py
└── requirements.txt

8 directories, 21 files
```
