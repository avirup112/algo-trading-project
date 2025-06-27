import os
import sys
import requests
import pandas as pd
from dotenv import load_dotenv

# Add module paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_fetcher import DataFetcherFactory
from strategy import TradingStrategy

# Load .env
load_dotenv()

class TelegramNotifier:
    """
    Sends alerts to a Telegram chat using the Telegram Bot API.
    Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to be defined in the .env file.
    """

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        if not self.token or not self.chat_id:
            raise ValueError("Missing Telegram credentials in environment variables.")

    def send_alert(self, message: str):
        """
        Send a message to the Telegram chat.
        """
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        try:
            response = requests.post(self.api_url, data=payload)
            if response.status_code != 200:
                print(f"[Telegram Error] {response.text}")
        except Exception as e:
            print(f"[Telegram Exception] {e}")


# Example Usage#
if __name__ == "__main__":
    try:
        notifier = TelegramNotifier()
        fetcher = DataFetcherFactory.get_data_fetcher("alpha_vantage")

        stock_symbol = "RELIANCE.BSE"
        holding_period = 5

        notifier.send_alert(f"Starting strategy for {stock_symbol}")

        df = fetcher.get_daily_data(stock_symbol, outputsize="full")

        if df.empty:
            notifier.send_alert(f"Failed to fetch data for {stock_symbol}")
        else:
            strategy = TradingStrategy(df)
            results = strategy.backtest_signals(holding_period=holding_period)

            if results.empty:
                notifier.send_alert(f"No trade signals found for {stock_symbol}")
            else:
                last_trade = results.iloc[-1]
                message = (
                    f"BUY Signal for {stock_symbol}\n"
                    f"Buy Date: {last_trade['Buy Date']}\n"
                    f"Buy Price: ₹{last_trade['Buy Price']}\n"
                    f"Sell Date: {last_trade['Sell Date']}\n"
                    f"Sell Price: ₹{last_trade['Sell Price']}\n"
                    f"Profit: ₹{last_trade['Profit ₹']} ({last_trade['Result']})"
                )
                notifier.send_alert(message)

    except Exception as e:
        print(f"[ERROR] {e}")
        TelegramNotifier().send_alert(f"❌ Error occurred in trading logic: {e}")
