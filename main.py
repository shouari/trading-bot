import pandas as pd
import streamlit as st
from datetime import datetime, date
import pycron
from pytz import timezone
import time
from get_postions import get_positions
from market_info import account_state
from operations import buy_operation, close_position
from trading_algo import get_moving_averages


tickers =['WIRE','KO', 'CLPS', 'TSLA', 'ROK', 'SPY', 'BTC-USD']


def trading(tickers):
    st.write("Starting the trading algo")
    while True:
        if pycron.is_now('* * * * 1-5', dt=datetime.now(timezone('EST'))):
            for ticker in tickers:
                SMA_9, SMA_30 = get_moving_averages(ticker)
                if SMA_9 > SMA_30:

                    # We should buy if we don't already own the stock
                    if ticker not in [i["symbol"] for i in get_positions()]:
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
                time.sleep(60)  # Making sure we don't run the logic twice in a minute
            # else:
            #     time.sleep(20)  # Check again in 20 seconds
            print("checking again in 15mn")
    return

st.title("Trading Bot")


# Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )
with st.container():
    st.write("Account status as of:", date.today())
    df = pd.DataFrame.from_dict(account_state(),orient="index", columns=["Value"])
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



