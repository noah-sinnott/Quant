
import os
from datetime import datetime ,timedelta
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest, MarketOrderRequest, TrailingStopOrderRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus, TimeInForce, OrderType
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockLatestTradeRequest
from alpaca.data.timeframe import TimeFrame


historical_data_client = StockHistoricalDataClient(os.environ['APCA_API_KEY_ID'], os.environ['APCA_API_SECRET_KEY'])
trading_client = TradingClient(os.environ['APCA_API_KEY_ID'], os.environ['APCA_API_SECRET_KEY'], paper=True)

def get_all_positions():
    try:
        positions = trading_client.get_all_positions()
        if positions:
            return positions
        else:
            print("No open positions.")
            return False
    except Exception as e:
        print("Failed to fetch positions:", e)

    
def get_last_order_details(symbol):
    try:
        temp = GetOrdersRequest(
                status=QueryOrderStatus.ALL,
                direction='desc',
                symbols=[symbol],
                side=OrderSide.BUY
            )
        orders = trading_client.get_orders(filter=temp)
        if orders:
            last_order = orders[0] 
            return last_order
        else:
            print(f"No orders found for {symbol}.")
            return False
            
    except Exception as e:
        print(f"Error fetching last order details for {symbol}: {e}")



def buy_stock(symbol, qty, id = None):

    temp = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        client_order_id=id,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY
    )
    market_order = trading_client.submit_order(
                order_data=temp
               )    
    print("Bought", qty, symbol)

def add_stop_loss(symbol, qty):
    
    temp = GetOrdersRequest(
                status=QueryOrderStatus.OPEN,
                direction='desc',
                side=OrderSide.SELL,
                symbols=[symbol],
            )
    orders = trading_client.get_orders(filter=temp)
    for order in orders:
        if order.type == OrderType.TRAILING_STOP:
            
            if(order.qty == qty):
                return
            
            cancled = trading_client.cancel_order_by_id(order.id)

    trailing_stop_pct = 2  # 2% trailing stop

    trailing_stop_order = TrailingStopOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,  # For selling the bought shares
        trail_percent=trailing_stop_pct,  # Trailing stop percentage
        time_in_force=TimeInForce.GTC  # 'Good Till Cancel' order type
    )

    trailing_stop_order_result = trading_client.submit_order(order_data=trailing_stop_order)
    print(f"Updated trailing stop loss of {trailing_stop_pct}% set for {symbol} with total qty {qty}")


def get_account_balance():
    temp = trading_client.get_account()
    return temp.cash

def sell_all_stock(symbol):
    temp = trading_client.close_position(symbol)
    print("Sold all", symbol)


def sell_stock(symbol, qty, id = None):
    temp = MarketOrderRequest(
        symbol=symbol,
        notional=qty,
        client_order_id=id,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.GTC
    )
    market_order = trading_client.submit_order(
                order_data=temp
             )    
    print("Sold", qty, symbol)


def get_asset(ticker):
    try:
        asset = trading_client.get_asset(ticker)
        return asset
    except Exception as e:
        return False
    
def get_asset_price(ticker):
    request = StockLatestTradeRequest(symbol_or_symbols=ticker)
    latest_trade = historical_data_client.get_stock_latest_trade(request)
    return latest_trade[ticker].price
#

