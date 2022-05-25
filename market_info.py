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
# print(type(account_state()))
# print(account_state())

# Later functionality to be added (ability to add new ticker)
# def check_stock():
#     for t in ["MSFT", "FAKE"]:
#         ticker = yf.Ticker(t)
#         info = None
#         try:
#             info = ticker.info
#         except:
#             print(f"Cannot get info of {t}, it probably does not exist")
#             continue
#
#         # Got the info of the ticker, do more stuff with it
#         print(f"Info of {t}: {info}")
# check_stock()
