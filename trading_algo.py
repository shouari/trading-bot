import requests
import json
import yfinance as yf
import pycron
import time
from datetime import datetime
from pytz import timezone
from get_postions import get_positions
from operations import buy_operation, close_position

CONFIG = json.load(open("./config.json"))
API_KEY, SECRET_KEY, BASE_URL = CONFIG["API_KEY"], CONFIG["SECRET_KEY"], CONFIG["BASE_URL"]


def get_moving_averages(ticker):
#   """
#   calculates the 9 day and 30 days moving average of the specified ticker
#   :param ticker: stock ticker
#   :return: returns (9 days moving average, 30 days moving average)
#   """
    data = yf.download(ticker, period="max", interval='1d')  # Download the last 3months worht of data for the ticker
    data['SMA_9'] = data['Close'].rolling(window=9, min_periods=1).mean()   # Compute a 9-day Simple Moving Average with pandas
    data['SMA_30'] = data['Close'].rolling(window=30, min_periods=1).mean()  # Compute a 30-day Simple Moving Average with pandas
    SMA_9 = float(data.tail(1)["SMA_9"])  # Get the latest calculated 9 days Simple Moving Average
    SMA_30 = float(data.tail(1)["SMA_30"]) # Get the latest 30 days Simple Moving Average
    return SMA_9, SMA_30

