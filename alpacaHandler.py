from alpaca_trade_api import REST
import os

alpaca = REST(os.environ['APCA_API_KEY_ID'], os.environ['APCA_API_SECRET_KEY'])

def buy_stock(symbol, qty, id = None):
    temp = alpaca.submit_order(
        symbol=symbol,
        notional=qty,
        client_order_id=id,
        side='buy',
        type='market',
        time_in_force='day'
    )
    print("ATTEMPTED to buy", qty, symbol, temp)
    
def sell_all_stock(symbol):
    temp = alpaca.close_position(symbol)
    print("error when attempitng to sell all", symbol, temp)


def sell_stock(symbol, qty, id = None):
    temp = alpaca.submit_order(
        symbol=symbol,
        qty=qty,
        client_order_id=id,
        side='sell',
        type='market',
        time_in_force='day'
    )
    print("error when attempitng to sell", qty, symbol, temp)


def check_fractional_trading(ticker):
    try:
        asset = alpaca.get_asset(ticker)
        if asset.fractionable:
            print(f"{ticker} can be traded fractionally.")
            return True
        else:
            print(f"{ticker} cannot be traded fractionally.")
            return False
    except Exception as e:
        print(f"Error fetching asset details for {ticker}: {e}")
        return False