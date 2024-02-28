from alpaca_trade_api import REST
import os
import requests

alpaca = REST(os.environ['APCA_API_KEY_ID'], os.environ['APCA_API_SECRET_KEY'])

def get_news (start, end):
    print(start, end)
    return alpaca.get_news(start=start, end=end, limit=10, symbol=["*"])

# async def on_order_update(order):
#     if order.event == 'fill': 
#         await add_stop_loss(order.symbol)

def get_all_positions():
    try:
        positions = alpaca.list_positions()
        if positions:
            return positions
        else:
            print("No open positions.")
            return False
    except Exception as e:
        print("Failed to fetch positions:", e)

    
def get_last_order_details(symbol):
    try:
        orders = alpaca.list_orders(status='all', direction='desc', symbols=[symbol])
        if orders:
            last_order = orders[0] 
            return last_order
        else:
            print(f"No orders found for {symbol}.")
            return False
            
    except Exception as e:
        print(f"Error fetching last order details for {symbol}: {e}")



def buy_stock(symbol, qty, id = None):
    

    temp = alpaca.submit_order(
        symbol=symbol,
        notional=qty,
        client_order_id=id,
        side='buy',
        type='market',
        time_in_force="day"
    )
    print("Bought", qty, symbol)

def add_stop_loss (symbol, percent = 10):
    open_orders = alpaca.list_orders(status='open')
    for order in open_orders:
        if order.symbol == symbol and (order.order_type == 'stop' or order.order_type == 'trailing_stop'):
            alpaca.cancel_order(order.id)


    position = alpaca.get_position(symbol)
    total_shares_owned = position.qty

    print("adding stop loss", symbol, total_shares_owned)
    alpaca.submit_order(
        symbol=symbol,
        qty=total_shares_owned, 
        side='sell',
        type='trailing_stop',
        trail_percent=percent,
        time_in_force='gtc' 
    )
    

def sell_all_stock(symbol):
    temp = alpaca.close_position(symbol)
    print("Sold all", symbol)


def sell_stock(symbol, qty, id = None):
    temp = alpaca.submit_order(
        symbol=symbol,
        qty=qty,
        client_order_id=id,
        side='sell',
        type='market',
        time_in_force='day'
    )
    print("Sold", qty, symbol)


def get_asset(ticker):
    try:
        asset = alpaca.get_asset(ticker)
        return asset
    except Exception as e:
        return False