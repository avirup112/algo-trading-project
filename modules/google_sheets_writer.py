import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd 
import os

from strategy import TradingStrategy

class GoogleSheetsLogger:
    """
    A class to handle logging data to Google Sheets using gspread.
    """
    
    def __init__(self, sheet_name:str):
        """
        Intialize Google Sheets client and open the target spreadsheet

        Parameters:
        sheet_name (str): Name of the Google Spreadsheet
        """
        
        self.sheet_name = sheet_name
        self.client = self._authorize()
        
    def _authorize(self):
        """
        Authorize the client using credentials.json
        
        Returns:
        gspread client object
        """
        
        scope=[
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds_path = os.path.join(os.path.dirname(__file__), "..", "credentials.json")
        
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
            return gspread.authorize(creds)
        except Exception as e:
            print(f"failed to open spreadsheet '{self.sheet_name}':{e}")
            raise
        
    def write_dataframe(self, df: pd.DataFrame, tab_name: str):
        """
        Write a pandas DataFrame to a specific tab in the Google Sheet.

        Parameters:
        df (pd.DataFrame): DataFrame to write
        tab_name (str): Name of the sheet tab to write to
        """
        try:
            spreadsheet = self.client.open(self.sheet_name)
        except Exception as e:
            print(f"Failed to open spreadsheet '{self.sheet_name}': {e}")
            return

        try:
            try:
                worksheet = spreadsheet.worksheet(tab_name)
                worksheet.clear()
            except gspread.exceptions.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(title=tab_name, rows="1000", cols="20")

            set_with_dataframe(worksheet, df)
            print(f"Data successfully written to Google Sheets tab: '{tab_name}'")

        except Exception as e:
            print(f"Failed to write data to Google Sheets tab '{tab_name}': {e}")


#Example usage
if __name__ == "__main__":
    from data_fetcher import DataFetcherFactory
    from google_sheets_writer import GoogleSheetsLogger
    import pandas as pd

    print("🚀 Fetching stock data...")
    fetcher = DataFetcherFactory.get_data_fetcher("alpha_vantage")
    df = fetcher.get_daily_data("RELIANCE.BSE", outputsize="full")

    if df.empty:
        print("No data fetched.")
    else:
        print("Data fetched. Running strategy...")

        strategy = TradingStrategy(df)
        results = strategy.backtest_signals(holding_period=5)

        if results.empty:
            print("No trade signals found.")
        else:
            print("\nSending to Google Sheets...")
            try:
                # ✅ Replace with your actual sheet name
                sheet_logger = GoogleSheetsLogger(sheet_name="Stock Signals")

                # Write trade log
                sheet_logger.write_dataframe(results, "Trade Log")

                # Write summary
                summary = pd.DataFrame({
                    "Total Trades": [len(results)],
                    "Win Ratio": [(results["Result"] == "Win").mean()],
                    "Total P&L (₹)": [results["Profit ₹"].sum()]
                })
                sheet_logger.write_dataframe(summary, "Summary")

            except Exception as e:
                print(f"Google Sheets logging failed: {e}")
     