from alpaca_trade_api import REST

alpaca = REST()

def buy_stock(symbol, qty):
    alpaca.submit_order(
        symbol=symbol,
        qty=qty,
        side='buy',
        type='market',
        time_in_force='day'
    )

def sell_all_stock(symbol):
    alpaca.close_position(symbol)


def sell_stock(symbol, qty):
    alpaca.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='market',
        time_in_force='day'
    )
