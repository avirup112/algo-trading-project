import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd 
import time
from alpha_vantage.timeseries import TimeSeries
from config import ALPHA_VANTAGE_API_KEY
from abc import ABC, abstractmethod



class StockDataFetcher(ABC):
    """
    Abstract base class for fetching stock data.

    """
    pass
    
    @abstractmethod
    def get_daily_data(self, symbol: str)-> pd.DataFrame:
        """
        Fetch daily stock data for a given symbol.

        Parameters:
        symbol (str): The stock ticker symbol

        Returns:
        pd.DataFrame: DataFrame containing daily stock data
        """
        pass
    
    @abstractmethod
    def get_intraday_data(self, symbol: str)-> pd.DataFrame:
        """
        Fetch intraday stock data for a given symbol.

        Parameters:
        symbol (str): The stock ticker symbol

        Returns:
        pd.DataFrame: DataFrame containing intraday stock data
        """
        pass
    
class AlphaVantageStockDataFetcher(StockDataFetcher):
    """
    Fetches stock data using Alpha Vintage API.

    Attributes:
    ts(TimeSeries): Intialized Alpha Vantage time series API Client.
    
    """
    
    def __init__(self, api_key=ALPHA_VANTAGE_API_KEY):
        """
        Intialize Alpha Vantage client.

        Args:
            api_key (str): Your Alpha Vantage API Key.
            
        """
        self.ts = TimeSeries(key=api_key, output_format='pandas')
        
    def get_daily_data(self,symbol: str, outputsize='compact') -> pd.DataFrame:
        """
        Fetch daily stock data for a given symbol.

        Parameters:
        symbol (str): Stock symbol.
        outputsize (str, optional): "compact" (last 100) or "full"(up to 20 years).

        Returns:
        pd.DataFrame: Clean and formatted stock data
        """
        
        try:
            data, _ = self.ts.get_daily(symbol=symbol, outputsize=outputsize)
            return self._format_data(data)
        except Exception as e:
            print(f"[ERROR]  failed to fetch daily data: {e}")
            return pd.DataFrame()
    
    def get_intraday_data(self, symbol: str, interval="15min", outputsize="compact"):
        """
        Fetch intraday stock data for a given symbol.

        Parameters:
        symbol (str): Stock symbol 
        interval (str): Time interval between two consecutive data points in the time series
        outputsize (str): "compact" returns only the latest 100 data points in the intraday time series
        Returns:
        pd.DataFrame: Cleaned intraday data.
        """
        try:
            data, _ = self.ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
            return self._format_data(data)
        except Exception as e:
            print(f"[ERROR] failed to fetch intraday data: {e}")
            return pd.DataFrame()
        
    def _format_data(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        format columns names and sort data

        Parameters:
        df (pd.DataFrame): Raw dataFrame

        Returns:
        pd.DataFrame: Cleaned DataFrame with renamed columns.
        """
        df.rename(columns={
            '1. open':'Open',
            '2. high':'High',
            '3. low':'Low',
            '4. close':'Close',
            '5. volume':'Volume',   
        }, inplace=True)
        df = df[::-1].reset_index()
        df.dropna(inplace=True)
        return df
    
class DataFetcherFactory:
    """
    Factory class to return appropriate StcokDataFetcher.
    
    Methods:
    get_data_fetcher(source: str) -> StockDataFetcher
    """
    
    @staticmethod
    def get_data_fetcher(source: str) -> StockDataFetcher:
        """
        Return a stock data fetcher based on source name.

        Parameters:
        source (str): Source name from where data is fetched

        Returns:
        StockDataFetcher: Concrete fetcher data
        """
        
        if source == "alpha_vantage":
            return AlphaVantageStockDataFetcher()
        else:
            raise ValueError(f"No data fetcher implemented for: {source}")

#Example usage       
if __name__ == "__main__":
    fetcher = DataFetcherFactory.get_data_fetcher("alpha_vantage")
    stocks = ["RELIANCE.BSE", "TCS.BSE", "INFY.BSE"]

    for stock in stocks:
        print(f"\nFetching daily data for {stock}...")
        df_daily = fetcher.get_daily_data(stock, outputsize="compact")
        print(df_daily.tail())

        print(f"\nFetching intraday data for {stock}...")
        df_intra = fetcher.get_intraday_data(stock, interval="15min")
        print(df_intra.tail())