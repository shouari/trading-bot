import pandas as pd
import streamlit as st
from datetime import datetime, date
import pycron
from pytz import timezone
import time
from get_postions import get_positions
from market_info import account_state,check_stock
from operations import buy_operation, close_position
from trading_algo import get_moving_averages


tickers =['WIRE','KO', 'CLPS', 'TSLA', 'ROK', 'SPY', 'BTC-USD']
buying_power = account_state()['Buying Power (US$)']

def trading(tickers):

    while True:
        if pycron.is_now('* 9-15 * * 1-5', dt=datetime.now(timezone('EST'))):
            st.write("Starting the trading algo")
            for ticker in tickers:
                SMA_9, SMA_30 = get_moving_averages(ticker)
                ticker_text = f'<p style="font-family:sans-serif; color:black; font-size: 12px;"><b><i>Information about {ticker}</i></b></p>'
                st.markdown(ticker_text, unsafe_allow_html=True)
                df = pd.DataFrame.from_dict(check_stock(ticker), orient="index", columns=["Value"])
                df = df.astype(str)
                st.table(df)
                if SMA_9 > SMA_30:
                    # We should buy if we don't already own the stock
                    if ticker not in [i["symbol"] for i in get_positions()]:
#add the check for buying power
                        st.write("Currently buying", ticker)
                        buy_operation(ticker, 1)
                    else:  # If position in portfolio we reinforce it
                        st.write("Currently reinforcing position", ticker)
                        buy_operation(ticker, 1)
                if SMA_9 < SMA_30:
                                        # We should liquidate our position if we own the stock
                    if ticker in [i["symbol"] for i in get_positions()]:
                        st.write("Currently liquidating our", ticker, "position")
                        close_position(ticker)
                    else:
                        st.write(f"No need to buy {ticker} at the time")
                time.sleep(900)  # Making sure we don't run the logic twice in a minute
            # else:
            #     time.sleep(20)  # Check again in 20 seconds
        return

st.title("Trading Bot")
st.write("The bot is trading every 15mn")

# Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )
with st.container():#table containing the account summary
    st.write("Account status as of:", date.today())
    df = pd.DataFrame.from_dict(account_state(),orient="index", columns=["Value"])
    df = df.astype(str)
    st.table(df)

with st.container():#table containing the positions summary
    st.write("Positions as of:", date.today())
    positions_summary = {'Symbol': [], 'Quantity': [], 'Average Entry Price': [], 'Market Value': []}
    for position in get_positions():
        positions_summary['Symbol'].append(position['symbol'])
        positions_summary['Quantity'].append(position['qty'])
        positions_summary['Average Entry Price'].append(position['avg_entry_price'])
        positions_summary['Market Value'].append(position['market_value'])

    df = pd.DataFrame.from_dict(positions_summary,orient="index")
    df = df.astype(str)
    st.table(df)

with st.sidebar:
    # add_radio = st.radio(
    #     "Choose a shipping method",
    #     ("Standard (5-15 days)", "Express (2-5 days)")
    # )
    st.write("Traded stock are:")
    for ticker in tickers:
        tickerstr = f'<p style="font-family:sans-serif; color:black; font-size: 12px;"><b><i>{ticker}</i></b></p>'
        st.markdown(tickerstr, unsafe_allow_html=True)

with st.container():
    trading(tickers)



