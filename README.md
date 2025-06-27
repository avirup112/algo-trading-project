<h1 align="center">Algo-trading-project</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/avirup112/algo-trading-project?color=56BEB8">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/avirup112/algo-trading-project?color=56BEB8">
  <img alt="License" src="https://img.shields.io/github/license/avirup112/algo-trading-project?color=56BEB8">
</p>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/avirup112" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

This project is an algorithmic trading automation system that fetches real-time stock data, executes a Moving Average + RSI strategy, and sends Telegram alerts for trade signals and outcomes. It also includes a basic machine learning model for trade prediction.

## :sparkles: Features ##

:heavy_check_mark: Fetch daily & intraday stock data using Alpha Vantage API:heavy_check_mark: Apply RSI + MA crossover strategy:heavy_check_mark: Backtest trades with P&L calculation:heavy_check_mark: Send Telegram alerts for signals and errors:heavy_check_mark: ML-based trade prediction using Logistic Regression

## :rocket: Technologies ##

- Python
- Pandas & NumPy
- Alpha Vantage API
- Python Dotenv
- Telegram Bot API
- Telegram Chat ID
- Scikit-learn
- gspread 
- Jupyter Notebook

## :white_check_mark: Requirements ##

Before starting, ensure you have:

- Git & Python installed
- A Telegram bot token and chat ID
- Alpha Vantage API key

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/avirup112/algo-trading-project

# Access
$ cd algo_trading_project

### 🔑 Environment Variables

Create your `.env` file from the example provided in the repo:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env

### 🔐 Google Sheets Integration

This project uses a Google Service Account to log data to Google Sheets.

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Google Sheets API** and **Google Drive API**.
3. Create a **Service Account** and download the `credentials.json` file.
4. Share the target Google Sheet with the service account email (something like `xxxx@xxxx.iam.gserviceaccount.com`).
5. Place the downloaded `credentials.json` in the root directory of the project.

# Install dependencies
$ pip install -r requirements.txt

# Run Jupyter Notebook ()
$ jupyter notebook auto_strategy_logger.ipynb
```

## :memo: License ##

This project is under the MIT License. For more details, see the [LICENSE](LICENSE) file.

Made by <a href="https://github.com/avirup112" target="_blank">Avirup Dasgupta</a>