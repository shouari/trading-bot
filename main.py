import time
import pandas as pd
import asyncio
import streamlit as st
from datetime import datetime, date
import pycron
from pytz import timezone
from get_postions import get_positions
from market_info import account_state, check_stock
from operations import trade_bot, dashboard
import logging

trade_history = "trade_history.txt"
logging.basicConfig(filename=trade_history, filemode= "w" ,level=logging.INFO)

if __name__ == "__main__":
    trade_history = "trade_history.txt"
    logging.basicConfig(filename='C:\\Users\\SalimHouari\\Documents\\Pycharm projects\\trading-bot\\trading_history.txt', filemode="a", level=logging.INFO, force=True)
    logger = logging.getLogger()
    st.set_page_config(page_title="Trading Bot", layout="wide", page_icon="🤖")
    title = st.empty()
    header = st.empty()
    title.title("Trading Bot")
    header.header("The bot is trading every 15mn")
    with st.sidebar:
        side_title = st.empty()
        ticker_lable = st.empty()
    # ['WIRE', 'KO', 'CLPS', 'TSLA', 'ROK', 'SPY', 'VOO']
    tickers = ['WIRE']
    account_header = st.empty()
    account_overview = st.empty()
    positions_header = st.empty()
    positions_hold = st.empty()
    positions_table = st.empty()
    with st.sidebar:
        side_title = st.empty()
        side_title.header("Traded stock are:")
        for ticker in tickers:
            tickerstr = f'<p style="font-family:sans-serif; color:black; font-size: 12px;"><b><i>{ticker} : {check_stock(ticker)["Long Name"]}</i></b></p> '
            st.markdown(tickerstr, unsafe_allow_html=True)
    while True:
        # ['WIRE','KO', 'CLPS', 'TSLA', 'ROK', 'SPY','VOO']

        asyncio.run(dashboard(account_header, account_overview, positions_header, positions_hold))

        if pycron.is_now('* 9-15 * * 1-5', dt=datetime.now(timezone('EST'))):

            st.markdown(
                """
            <style>
            .time {
                font-size: 20px !important;
                font-weight: 700 !important;
                color: #ec5953 !important;
            }
            </style>
            """,
                unsafe_allow_html=True
            )
            bot_start = st.empty()
            ticker_info = st.empty()

            asyncio.run(
                trade_bot(bot_start, ticker_info, positions_table))
            time.sleep(60*15)
            continue
        else:
            st.markdown(
                """
    
                <style>
                .time {
                    font-size: 20px !important;
                    font-weight: 700 !important;
                    color: 	#FF0000 !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            async def open_market(close):
                with st.container():  # table containing the account summary
                    close.markdown(
                        f"""
                        <p class="time">
                            US market closed at this time
                        </p>
                        """, unsafe_allow_html=True)
                    r = await asyncio.sleep(5)
                    logger.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : US market closed at this time')
            close = st.empty()
            asyncio.run(open_market(close))
        time.sleep(60*60)
        continue
