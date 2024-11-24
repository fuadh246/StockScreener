

import os
import pandas as pd
import numpy as np
import sqlite3

# pip install pandas-datareader
import pandas_datareader as pdr

import yfinance as yf

import option

from stock import Stock

import warnings
warnings.filterwarnings('ignore')

# https://www.geeksforgeeks.org/python-stock-data-visualisation/

class Loader(object):

    def __init__(self, opt, db_connection):
        # opt is the option 
        self.opt = opt
        self.db_connection = db_connection

    def get_daily_from_yahoo(self, ticker, start_date, end_date):
        stock = yf.Ticker(ticker)
        df = stock.history(start = start_date, end = end_date, interval = '1d')
        df['Ticker'] = ticker
        return(df)

    def download_data_to_csv(self, list_of_tickers):
        if not os.path.exists(self.opt.output_dir):
            os.makedirs(self.opt.output_dir)
            print(f"Created directory: {opt.output_dir}")
        
        for ticker in list_of_tickers:
        # Call get_daily_from_yahoo for each ticker
            df = self.get_daily_from_yahoo(ticker, self.opt.start_date, "2024-10-08")
            if df is not None:
                # Save the DataFrame to a CSV file in the output_dir
                output_file = os.path.join(self.opt.output_dir, f"{ticker}_daily.csv")
                print(f"Saving {ticker} data to {output_file}")
                df.to_csv(output_file, index=True)  # Write to CSV
                print(f"Saved {ticker} data to {output_file}")
        
        
        
    def csv_to_table(self, csv_file_name, fields_map, db_table):
        # insert data from a csv file to a table
        df = pd.read_csv(csv_file_name)
        if df.shape[0] <= 0:
            return
        
        # change the column header to match how they are spelled in the database
        df.columns = [fields_map.get(x, x) for x in df.columns]
        print(df.columns)

        # move ticker columns
        # new_df = df[['Ticker']]
        # for c in df.columns[:-1]:
        #     new_df[c] = df[c]

        ticker = os.path.basename(csv_file_name).replace('.csv','').replace("_daily", "")
        print(ticker)
        cursor = self.db_connection.cursor()

        '''
        Delete from the table any old data for the ticker
        hint: sql = f"delete from {db_table} .... ", then call execute
        turn the dataframe into tuples
        
        insert data by using a insert ... values statement under executemany method
        hint: sql = f"insert into {db_table} (Ticker, AsOfDate, ...)  VALUES (?, ?, ...) "
        print(sql)

        remember to close the db connection
        
        '''
        sql_delete = f"DELETE FROM {db_table} WHERE Ticker = ?"
        # cursor.execute(sql_delete, (ticker,))
        cursor.execute(sql_delete, (df['Ticker'][0],))
        
        # insert new data
        sql_insert = f"""INSERT INTO {db_table} 
                        (Ticker, AsOfDate, Open, High, Low, Close, Volume, Dividend, StockSplits) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        data_tuples = [tuple(x) for x in df[['Ticker', 'AsOfDate', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividend', 'StockSplits']].values]
        
        cursor.executemany(sql_insert, data_tuples)
        self.db_connection.commit()
        print(f"Inserted data for {ticker} into {db_table}")

    def save_daily_data_to_sqlite(self, daily_file_dir, list_of_tickers):
        # read all daily.csv files from a dir and load them into sqlite table
        db_table = 'EquityDailyPrice'
        db_file = os.path.join(self.opt.sqlite_db)
        db_conn = sqlite3.connect(db_file)

        # define a fields_map dictionary to map the column name of the csv file to what is expected in the database table

        fields_map = {
            'Date': 'AsOfDate',
            'Open': 'Open',
            'High': 'High',
            'Low': 'Low',
            'Close': 'Close',
            'Volume': 'Volume',
            'Dividends': 'Dividend',
            'Stock Splits': 'StockSplits'
        }
        
        for ticker in list_of_tickers:
            file_name = os.path.join(daily_file_dir, f"{ticker}_daily.csv")
            print(file_name)
        # check if the file exists
            if os.path.isfile(file_name):
                self.csv_to_table(file_name, fields_map, db_table)
            else:
                print(f"File not found: {file_name}")
        

        
    def save_daily_TA_data_to_sqlite(self, input_df):
        # On accepting a dataframe with columns, Ticker, AsOfDate, Close, Volume, SMA10, ...
        # upload the TA values to the EquityTechnicalIndicators table
        db_table = "EquityTechnicalIndicators"
        cursor = self.db_connection.cursor()
        
        fields_map = {
            'Ticker': 'Ticker',
            'AsOfDate': 'AsOfDate',
            'Close':'Close',
            'Volume': 'Volume',
            'SMA_10': 'SMA10',
            'SMA_20': 'SMA20',
            'SMA_50':'SMA50',
            'SMA_200':'SMA200',
            'RSI':'RSI',
            'MACDline': 'MACDline',
            'MACDsignal': 'MACDsignal',
            'BBupperBand': 'BBupperBand',
            'BBmiddleBand': 'BBmiddleBand',
            'BBlowerBand': 'BBlowerBand',
            'ADX': 'ADX',
            'DMP': 'DMP',
            'DMN':'DMN'
        }
        input_df.columns = [fields_map.get(x, x) for x in input_df.columns]
        # filter necessary columns
        upload_df = input_df[list(fields_map.values())]

        sql_delete = f"DELETE FROM {db_table} WHERE Ticker = ?"
        cursor.execute(sql_delete, (upload_df['Ticker'].iloc[0],))
        
        # insert statement
        sql_insert = f"""
            INSERT INTO {db_table} (
                Ticker, AsOfDate, Close, Volume, SMA10, SMA20, SMA50, SMA200,
                RSI, MACDline, MACDsignal, BBupperBand, BBmiddleBand, BBlowerBand,
                ADX, DMP, DMN
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # convert the dataFrame to a list of tuples for insertion
        data_tuples = [tuple(row) for row in upload_df.to_records(index=False)]
        
        cursor.executemany(sql_insert, data_tuples)
        
        self.db_connection.commit()
        print(f"Inserted data for {input_df.name} into {db_table}")
        

    def calc_and_upload_TA_indicators(self, list_of_tickers):
        '''
        For each ticker
        1. create a stock object, download the pricing data from the EquityDailyPrice table
        2. calc all the necessary TA
        3. upload the data in the dataframe to the EquityTechnicalIndicators table

        '''
        for ticker in list_of_tickers:
           stock = Stock(self.opt, self.db_connection, ticker=ticker)

           stock.get_daily_hist_price_from_db(self.opt.start_date, self.opt.end_date)
           stock.calc_all_TA_indicators()
           df = stock.ohlcv_df
           self.save_daily_TA_data_to_sqlite(df)

        
        
def run():
    #
    parser = option.get_default_parser()
    parser.add_argument('--data_dir', dest = 'data_dir', default='./data', help='data dir')    
    
    args = parser.parse_args()
    opt = option.Option(args = args)

    opt.output_dir = os.path.join(opt.data_dir, "daily")
    opt.sqlite_db = os.path.join(opt.data_dir, "sqlite/Equity.db")
    
    if opt.tickers is not None:
        list_of_tickers = opt.tickers.split(',')
    else:
        fname = os.path.join(opt.data_dir, "S&P500.csv")
        df = pd.read_csv(fname)
        list_of_tickers = list(df['Symbol'])
        print(f"Read tickers from {fname}")

    print(list_of_tickers)
    print(opt.start_date, opt.end_date)

    db_file = opt.sqlite_db
    db_connection = sqlite3.connect(db_file)
    
    loader = Loader(opt, db_connection)
    print(f"Download data to {opt.data_dir} directory")

    # Turn the flag from 1 to 0 after you are done with testing for faster development
    if 0:
        # download data to csv files
        loader.download_data_to_csv(list_of_tickers)

    if 0:
        loader.save_daily_data_to_sqlite(opt.output_dir, list_of_tickers)

    if 1:
        loader.calc_and_upload_TA_indicators(list_of_tickers)
    
if __name__ == "__main__":
    #_test()
    run()
