import requests
import json
import yfinance as yf


CONFIG = json.load(open("./config.json"))
API_KEY, SECRET_KEY, BASE_URL = CONFIG["API_KEY"], CONFIG["SECRET_KEY"], CONFIG["BASE_URL"]

def account_state():
    url = BASE_URL + "/v2/account"
    headers = {
        'APCA-API-KEY-ID': API_KEY,
        'APCA-API-SECRET-KEY': SECRET_KEY,
        'Content-Type': 'application/json'
    }
    account_info = requests.request("GET", url, headers=headers).json()
    account_status = {
        "Buying Power (US$)": "{:,.2f}".format(float(account_info["buying_power"])),
        "Cash (US$)": "{:,.2f}".format(float(account_info["cash"])),
        "Daytrade Count":"{:,}".format(int(account_info["daytrade_count"])),
        "Portfolio Value (US$)":"{:,.2f}".format(float(account_info["portfolio_value"]))
    }
    return account_status


# Later functionality to be added (ability to add new ticker)
def check_stock(ticker):
    ticker_info = yf.Ticker(ticker)
    info = None
    info_bulk =None
    try:
        info_bulk = ticker_info.info
        info = {
            "Symbol": ticker_info.info['symbol'],
            "Long Name": ticker_info.info['longName'],
            "Enterprise Revenue": ticker_info.info['enterpriseToRevenue'],
            "Revenue Quarter Growth": ticker_info.info['revenueQuarterlyGrowth'],
            "Total Assets": ticker_info.info['totalAssets'],
            "3 Years Ave. return": ticker_info.info['threeYearAverageReturn'],
            "Regular market previous close": ticker_info.info['regularMarketPreviousClose'],
            "Open": ticker_info.info['open'],
            "Market Cap": ticker_info.info['marketCap'],
            "Regular Market Price": ticker_info.info['regularMarketPrice']
        }
        print(type(info))
    except:
        print(f"Cannot get info of {ticker}, it probably does not exist")
     # Got the info of the ticker, do more stuff with it
    return info


