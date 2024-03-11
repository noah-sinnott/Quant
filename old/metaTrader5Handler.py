import requests
import os
import json
import MetaTrader5 as mt5
from datetime import datetime ,timedelta

MT5_USERNAME = os.environ['MT5_USERNAME']
MT5_PASSOWRD = os.environ['MT5_PASSOWRD']
MT5_SERVER =  os.environ['MT5_SERVER']


def initialise_meta_trader_5():
    mt5.shutdown()
    timeout = 10000
    portable = False
    if not mt5.initialize(login=1520120527, password=MT5_PASSOWRD,server=MT5_SERVER, timeout=timeout, portable=portable):
        print("initialize() failed, error code =", mt5.last_error())
    else:
        mt5.login(login=MT5_USERNAME, password=MT5_PASSOWRD, server=MT5_SERVER)
    

def get_all_positions():
    try:
        positions = mt5.positions_get()
        print("positions: ", positions)

        if positions:
            return positions
        else:
            print("No open positions.")
            return False
    except Exception as e:
        print("Failed to fetch positions:", e)

    
def get_last_order_details(symbol):
    try:
        orders = mt5.orders_get(symbol=symbol)
        print("orders: ", orders)

        if orders:
            last_order = orders[0] 
            return last_order
        else:
            print(f"No orders found for {symbol}.")
            return False
            
    except Exception as e:
        print(f"Error fetching last order details for {symbol}: {e}")



def buy_stock(symbol, qty, id = None):

    rounded = round(qty, 2)
    stockToBuy = 1
    t = mt5.symbol_select(symbol, True)
    symbolInfo = mt5.symbol_info(symbol)
    symbolInfoTick = mt5.symbol_info_tick(symbol)

    print(qty, symbolInfo, symbolInfoTick, t, symbol)
    point = symbolInfo.point
    price = symbolInfoTick.ask

    deviation = 20

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": stockToBuy,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": id,
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    print("from buying ", request)
    return
    result = mt5.order_send(request)

    print("Bought", qty, symbol)


def get_account_balance():
    temp = mt5.account_info()
    print("account info: ", temp)
    return temp.balance

def sell_all_stock(symbol):
    temp = mt5.Close(symbol)
    print("from selling all", temp)
    print("Sold all", symbol)
