import requests
import json
import yfinance as yf
import pycron
import time
from datetime import datetime
from pytz import timezone

CONFIG = json.load(open("./config.json"))
API_KEY, SECRET_KEY, BASE_URL = CONFIG["API_KEY"], CONFIG["SECRET_KEY"], CONFIG["BASE_URL"]

def get_positions():

#   sends a GET request to "/v2/positions" and returns the current positions that are open in our account
#   :return: the positions that are held in the alpaca trading account

    url = BASE_URL + "/v2/positions"
    headers = {
        'APCA-API-KEY-ID': API_KEY,
        'APCA-API-SECRET-KEY': SECRET_KEY,
    }
    positions = requests.request("GET", url, headers=headers).json()


    return positions


