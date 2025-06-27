<h1 align="center">Algo_Trading_Project</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/avirup112/algo_trading_project?color=56BEB8">
  <img alt="Github language count" src="https://img.shields.io/github/languages/count/avirup112/algo_trading_project?color=56BEB8">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/avirup112/algo_trading_project?color=56BEB8">
  <img alt="License" src="https://img.shields.io/github/license/avirup112/algo_trading_project?color=56BEB8">
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

This project is an **automated algorithmic trading assistant** built using Python and Alpha Vantage API. It implements a basic RSI + Moving Average crossover strategy, performs backtesting, and sends Telegram alerts based on trade signals or errors.

## :sparkles: Features ##

:heavy_check_mark: Fetch stock data from Alpha Vantage API;\
:heavy_check_mark: Apply technical analysis (RSI, MA20, MA50);\
:heavy_check_mark: Simulate trades with backtesting;\
:heavy_check_mark: Send Telegram alerts for BUY signals and errors;\
:heavy_check_mark: Jupyter Notebook integration for analysis and reporting.

## :rocket: Technologies ##

The following tools/libraries were used in this project:

- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Alpha Vantage API](https://www.alphavantage.co/)
- [Requests](https://docs.python-requests.org/)
- [Python Telegram Bot](https://core.telegram.org/bots/api)
- [Jupyter Notebook](https://jupyter.org/)

## :white_check_mark: Requirements ##

Before starting, make sure you have:

- Python 3.8 or higher installed
- `pip` for installing dependencies
- Alpha Vantage API Key
- Telegram Bot Token and Chat ID

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/avirup112/algo_trading_project

# Access
$ cd algo_trading_project

# Create virtual environment
$ python -m venv venv
$ venv\Scripts\activate  # On Windows

# Install dependencies
$ pip install -r requirements.txt

# Setup environment variables
$ copy .env.example .env
# Then add your API keys to .env

# Run notebook
$ jupyter notebook auto_strategy_logger.ipynb
