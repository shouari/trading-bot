import pandas as pd
import asyncio
import streamlit as st
from datetime import datetime, date
import pycron
from pytz import timezone
from get_postions import get_positions
from market_info import account_state,check_stock
from operations import buy_operation, close_position, buying_check
from trading_algo import get_moving_averages

# , 'CLPS', 'TSLA', 'ROK', 'SPY', 'BTC-USD'

tickers =['WIRE','KO', 'CLPS', 'TSLA', 'ROK', 'SPY','VOO']


st.title("Trading Bot")
st.write("The bot is trading every 15mn")
with st.sidebar:
    st.write("Traded stock are:")
    for ticker in tickers:
        tickerstr = f'<p style="font-family:sans-serif; color:black; font-size: 12px;"><b><i>{ticker} : {check_stock(ticker)["Long Name"]}</i></b></p>'
        st.markdown(tickerstr, unsafe_allow_html=True)

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

    async def trade_bot(account_header, account_overview, positions_header, positions_hold,bot_start,ticker_info, positions_table):
        with st.container():  # table containing the account summary
            while True:
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

                bot_start.write("Starting the trading algorithm")
                for ticker in tickers:
                    SMA_9, SMA_30 = get_moving_averages(ticker)
                    ticker_text = f'<p style="font-family:sans-serif; color:black; font-size: 12px;"><b><i>Checking currently the stock  {ticker}</i></b></p>'
                    ticker_info.markdown(ticker_text, unsafe_allow_html=True)
                    df = pd.DataFrame.from_dict(check_stock(ticker), orient="index", columns=["Value"])
                    df = df.astype(str)
                    positions_table.table(df)
                    if SMA_9 > SMA_30:
                        if buying_check(ticker):
                        # We should buy if we don't already own the stock
                            if ticker not in [i["symbol"] for i in get_positions()]:
                                st.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : Currently buying  {ticker}')
                                buy_operation(ticker, 1)
                        else:
                            st.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : Not enough cash to buy : {ticker}')
                        # else:  # If position in portfolio we reinforce it
                        #     st.write("Currently reinforcing position", ticker)
                        #     buy_operation(ticker, 1)
                    if SMA_9 < SMA_30:
                        # We should liquidate our position if we own the stock
                        if ticker in [i["symbol"] for i in get_positions()]:
                            st.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : Currently liquidating our {ticker} position')
                            close_position(ticker)
                        else:
                            st.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : No need to buy {ticker} for the moment')
                    # time.sleep(900)  # Making sure we don't run the logic twice in a minute
                    # else:
                    #     time.sleep(20)  # Check again in 20 seconds
                r = await asyncio.sleep(900)



    account_header = st.empty()
    account_overview = st.empty()
    positions_header = st.empty()
    positions_hold = st.empty()
    bot_start = st.empty()
    ticker_info = st.empty()
    positions_table = st.empty()

    asyncio.run(trade_bot(account_header, account_overview, positions_header, positions_hold,bot_start,ticker_info,positions_table))

