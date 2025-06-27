import pandas as pd
import numpy as np
import sys
import os

from data_fetcher import DataFetcherFactory

# Add module path to import data_fetcher or other shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class TradingStrategy:
    """
    Implements an RSI + Moving Average crossover strategy.
    Generates BUY signals and simulates basic backtesting.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with stock price data.

        Parameters:
        df (pd.DataFrame): Historical stock data with 'Close' and 'date' columns.
        """
        self.df = df.copy()
        self.signals = pd.DataFrame()

    def compute_indicators(self):
        """
        Compute RSI (Relative Strength Index),
        20-day and 50-day moving averages for the DataFrame.
        """
        close = self.df['Close']
        delta = close.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()

        rs = avg_gain / (avg_loss + 1e-10)  # Avoid division by zero
        rsi = 100 - (100 / (1 + rs))
        self.df['RSI'] = rsi

        self.df['MA20'] = close.rolling(window=20).mean()
        self.df['MA50'] = close.rolling(window=50).mean()

    def generate_signals(self) -> pd.DataFrame:
        """
        Generate BUY signals based on:
        - RSI < 30
        - 20-day MA crossing above 50-day MA

        Returns:
        pd.DataFrame: DataFrame containing the buy signal rows
        """
        self.compute_indicators()
        buy_signals = []

        for i in range(1, len(self.df)):
            rsi = self.df.loc[i, 'RSI']
            ma20_prev = self.df.loc[i - 1, 'MA20']
            ma50_prev = self.df.loc[i - 1, 'MA50']
            ma20_now = self.df.loc[i, 'MA20']
            ma50_now = self.df.loc[i, 'MA50']

            if (
                pd.notna(rsi) and pd.notna(ma20_prev) and pd.notna(ma50_prev) and
                rsi < 30 and
                ma20_prev < ma50_prev and ma20_now > ma50_now
            ):
                buy_signals.append(self.df.loc[i, 'date'])

        self.signals = self.df[self.df['date'].isin(buy_signals)].copy()
        self.signals['Signal'] = 'BUY'
        return self.signals

    def backtest_signals(self, holding_period=5):
        """
        Backtest strategy with fixed holding period to calculate P&L.

        Args:
            holding_period (int): Days to hold the stock after buy signal.

        Returns:
            pd.DataFrame: Trade log with buy date, sell date, and profit/loss.
        """
        signals = self.generate_signals()
        trade_log = []

        for _, signal in signals.iterrows():
            buy_date = signal['date']
            buy_price = signal['Close']

            # Find index of buy_date in original df
            idx = self.df[self.df['date'] == buy_date].index[0]

            # Calculate sell index and handle edge case
            sell_idx = idx + holding_period
            if sell_idx >= len(self.df):
                continue  # Skip incomplete trades

            sell_date = self.df.loc[sell_idx, 'date']
            sell_price = self.df.loc[sell_idx, 'Close']
            profit = sell_price - buy_price
            result = "Win" if profit > 0 else "Loss"

            trade_log.append({
                "Buy Date": buy_date,
                "Buy Price": buy_price,
                "Sell Date": sell_date,
                "Sell Price": sell_price,
                "Profit ₹": round(profit, 2),
                "Result": result
            })

        return pd.DataFrame(trade_log)

    def backtest(self):
        """
        Print all BUY signals with indicators (without P&L logic).
        """
        signals = self.generate_signals()
        print("\nBuy signals found:")
        print(signals[['date', 'Close', 'RSI', 'MA20', 'MA50', 'Signal']])
        return signals
 
# Example usage   
if __name__ == "__main__":
    fetcher = DataFetcherFactory.get_data_fetcher("alpha_vantage")
    df = fetcher.get_daily_data("RELIANCE.BSE", outputsize="full")

    strategy = TradingStrategy(df)
    results = strategy.backtest_signals(holding_period=5)

    print("\nFinal Results:")
    print(results.tail())