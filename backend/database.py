import sqlite3
import pandas as pd
def connect_to_db(path):
    try:
        connection = sqlite3.connect(path)
        print(f"Connected to SQLite database at {path}")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        
def read_query_as_dataframe(connection, query, parameters=None):
    """
    Execute a SELECT query on the SQLite database and return results as a Pandas DataFrame.

    Args:
        connection (sqlite3.Connection): Connection object to the SQLite database.
        query (str): SQL SELECT query to execute.
        parameters (tuple, optional): Parameters to pass into the query.

    Returns:
        pd.DataFrame: Query results as a Pandas DataFrame.
    """
    try:
        if parameters:
            df = pd.read_sql_query(query, connection, params=parameters)
        else:
            df = pd.read_sql_query(query, connection)

        print("Query executed, DataFrame returned.")
        numeric_cols = df.select_dtypes(include=["float", "int"]).columns
        df[numeric_cols] = df[numeric_cols].round(2)
        connection.close()
        return df

    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
