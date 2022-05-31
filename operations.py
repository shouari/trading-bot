import requests
import json
import pandas as pd
import asyncio
import streamlit as st
from datetime import datetime, date
from get_postions import get_positions
from market_info import account_state, check_stock
from trading_algo import get_moving_averages


CONFIG = json.load(open("./config.json"))
API_KEY, SECRET_KEY, BASE_URL = CONFIG["API_KEY"], CONFIG["SECRET_KEY"], CONFIG["BASE_URL"]

tickers = ['WIRE', 'KO', 'CLPS', 'TSLA', 'ROK', 'SPY', 'VOO']


def buy_operation(ticker, quantity):
  """
  send a POST request to "/v2/orders" to create a new order
  :param ticker: stock ticker
  :param quantity:  quantity to buy
  :return: confirmation that the order to buy has been opened
  """
  url = BASE_URL + "/v2/orders"
  payload = json.dumps({
      "symbol": ticker,
      "qty": quantity,
      "side": "buy",
      "type": "market",
      "time_in_force": "day"
  })
  headers = {
      'APCA-API-KEY-ID': API_KEY,
      'APCA-API-SECRET-KEY': SECRET_KEY,
      'Content-Type': 'application/json'
  }
  return requests.request("POST", url, headers=headers, data=payload).json()

def close_position(ticker):

#   sends a DELETE request to "/v2/positions/" to liquidate an open position
#   :param ticker: stock ticker
#   :return: confirmation that the position has been closed

    url = BASE_URL + "/v2/positions/" + ticker

    headers = {
        'APCA-API-KEY-ID': API_KEY,
        'APCA-API-SECRET-KEY': SECRET_KEY
    }
    return requests.request("DELETE", url, headers=headers).json()

def buying_check(ticker):
    buying_power = float(account_state()['Buying Power (US$)'].replace(",",""))

    stock_price= float(check_stock(ticker)["Regular Market Price"])

    return True if buying_power>stock_price else False

async def trade_bot(bot_start, ticker_info,
                    positions_table):
    bot_start.write(f'Starting the trading algorithm at : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    for ticker in tickers:
        SMA_9, SMA_30 = get_moving_averages(ticker)
        ticker_text = f'<p style="font-family:sans-serif; color:black; font-size: 12px;"><b><i>Checking currently the stock  {ticker}</i></b></p>'
        ticker_info.markdown(ticker_text, unsafe_allow_html=True)
        df = pd.DataFrame.from_dict(check_stock(ticker), orient="index", columns=["Value"])
        df = df.astype(str)
        # positions_table.table(df)
        if SMA_9 > SMA_30:
            if buying_check(ticker):
                # We should buy if we don't already own the stock
                if ticker not in [i["symbol"] for i in get_positions()]:
                    st.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : Currently buying  {ticker}')
                    buy_operation(ticker, 1)
            else:
                st.write(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : Not enough cash to buy : {ticker}')
            # else:  # If position in portfolio we reinforce it
            #     st.write("Currently reinforcing position", ticker)
            #     buy_operation(ticker, 1)
        if SMA_9 < SMA_30:
            # We should liquidate our position if we own the stock
            if ticker in [i["symbol"] for i in get_positions()]:
                st.write(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : Currently liquidating our {ticker} position')
                close_position(ticker)
            else:
                st.write(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : No need to buy {ticker} for the moment')
            # time.sleep(900)  # Making sure we don't run the logic twice in a minute
            # else:
            #     time.sleep(20)  # Check again in 20 seconds
    ticker_info.empty()
    r = await asyncio.sleep(1)
    return

async def dashboard(account_header, account_overview, positions_header, positions_hold):
    with st.container():  # table containing the account summary
        account_header.markdown(
            f"""
        <p class="time">
            Account status as of :  {date.today()}
        </p>
        """, unsafe_allow_html=True)

        account = pd.DataFrame.from_dict(account_state(), orient="index", columns=["Value"])
        account = account.astype(str)
        account_overview.table(account)

        positions_header.markdown(
            f"""
            <p class="time">
                Positions hold as of : {date.today()}
            </p>
            """, unsafe_allow_html=True)

        positions_summary = {'Symbol': [], 'Quantity': [], 'Average Entry Price': [], 'Market Value': []}
        for position in get_positions():
            positions_summary['Symbol'].append(position['symbol'])
            positions_summary['Quantity'].append(position['qty'])
            positions_summary['Average Entry Price'].append(position['avg_entry_price'])
            positions_summary['Market Value'].append(position['market_value'])
        positions = pd.DataFrame.from_dict(positions_summary, orient="index")
        positions = positions.astype(str)
        positions_hold.table(positions)
    r = await asyncio.sleep(5)