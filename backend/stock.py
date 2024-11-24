

import os
import pandas as pd
import numpy as np
import math
import datetime 
import sqlite3

import pandas_ta as ta
from utils import MyYahooFinancials
import option

class Stock(object):
    '''
    Stock class for getting various data related to a single stock, including pricing, TA and fundamental data
    '''
    def __init__(self, opt, db_connection, ticker, rsi_period = 14, sma_periods = [10, 20, 50, 200],
                 spot_price = None, sigma = None, dividend_yield = 0, freq = 'annual'):
        self.opt = opt
        self.db_connection = db_connection
        self.ticker = ticker
        self.spot_price = spot_price
        self.sigma = sigma
        self.dividend_yield = dividend_yield

        self.rsi_period = rsi_period 
        self.sma_periods = sma_periods
        
        self.yfin = MyYahooFinancials(ticker, freq)
        

    #######################   The following methods are for getting pricing data 
    
    def get_daily_hist_price_from_db(self, start_date, end_date):
        # Get daily historical OHLCV from database
        try:
            sql = f"select * from EquityDailyPrice where ticker = '{self.ticker}' order by AsOfDate asc"
            df = pd.read_sql(sql, self.db_connection)
            df['AsOfDate'] = df['AsOfDate'].apply(lambda x: datetime.datetime.strptime(x[:10], "%Y-%m-%d").date())

            # filter data between start and end date
            df = df[ df.AsOfDate >= datetime.datetime.strptime(start_date, "%Y-%m-%d").date()]
            df = df[ df.AsOfDate <= datetime.datetime.strptime(end_date, "%Y-%m-%d").date()]

            # create an index based on the AsOfDate column
            df['Date'] = df.AsOfDate
            df = df.set_index('Date')
            
            self.ohlcv_df = df
            self.ohlcv_df.name = self.ticker
            return(df)
            
        except Exception as e:
            print(f"Failed to get data for {self.ticker}: {e}")
            raise Exception(e)

    def calc_daily_returns(self):
        # calculate daily return as percentage change of the daily price
        self.ohlcv_df['daily_returns'] = ((self.ohlcv_df['Close'] - self.ohlcv_df['Close'].shift(1)) / self.ohlcv_df['Close'].shift(1)) * 100
        
        
    ######################### The following methods are for calculating TA data ############

    def calc_all_TA_indicators(self):
        self.calc_sma()
        self.calc_rsi()
        self.calc_macd()
        self.calc_bbands()
        self.calc_adx()
        
        # end TODO

        
    def calc_sma(self):
        for period in self.sma_periods:
           self.ohlcv_df[f"SMA_{period}"] = self.ohlcv_df['Close'].rolling(window=period).mean()
        
        

    def calc_macd(self):
        fast= 12
        slow= 26
        signal= 9
        macd = ta.macd(self.ohlcv_df['Close'], fast=fast, slow=slow, signal=signal)

        self.ohlcv_df['MACDline'] = macd[f'MACD_{fast}_{slow}_{signal}']
        self.ohlcv_df['MACDsignal'] = macd[f'MACDs_{fast}_{slow}_{signal}']       
        
    def calc_rsi(self):
        self.ohlcv_df['RSI'] = ta.rsi(self.ohlcv_df['Close'], length=self.rsi_period)

    def calc_bbands(self):
        bbands = ta.bbands(self.ohlcv_df['Close'],length=20)
        self.ohlcv_df['BBupperBand'] = bbands['BBU_20_2.0']
        self.ohlcv_df['BBlowerBand'] = bbands['BBM_20_2.0']
        self.ohlcv_df['BBmiddleBand'] = bbands['BBL_20_2.0']

    def calc_adx(self):
        adx = ta.adx(self.ohlcv_df['High'], self.ohlcv_df['Low'], self.ohlcv_df['Close'])
        self.ohlcv_df['ADX'] = adx['ADX_14']
        self.ohlcv_df['DMP'] = adx['DMP_14']
        self.ohlcv_df['DMN'] = adx['DMN_14']
        
        
    #######################   The following methods are for funamental data #####################
    ##  To be added
    
    def load_financial_data(self):
        #
        print(f"Loading financial data for {self.ticker}")
        self.yfin.load_latest_data()
        
        

def _test():
    # a few basic unit tests
    parser = option.get_default_parser()
    parser.add_argument('--data_dir', dest = 'data_dir', default='./data', help='data dir')    
    
    args = parser.parse_args()
    opt = option.Option(args = args)

    opt.output_dir = os.path.join(opt.data_dir, "daily")
    opt.sqlite_db = os.path.join(opt.data_dir, "sqlite/Equity.db")

    db_file = opt.sqlite_db
    print(db_file)
    db_connection = sqlite3.connect(db_file)

    print(vars(opt))
    
    symbol = 'AAPL'
    stock = Stock(opt, db_connection, symbol)

    start_date = datetime.date(2012, 1, 1)
    end_date = datetime.date(2024, 10, 1)
    stock.get_daily_hist_price_from_db(start_date, end_date)
    stock.calc_all_TA_indicators()

    df = stock.ohlcv_df

    print(df.head(30))
    print(df.tail(10).to_csv("test.csv"))
    
    print(df.columns)
    
    
if __name__ == "__main__":
    _test()
