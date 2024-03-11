
from alpacaHandler import get_all_positions, get_last_order_details, buy_stock, sell_all_stock,get_asset_price, add_stop_loss
import math
import time
from datetime import datetime, timedelta, timezone
import math
import os

POSITION_MANAGMENT_SELL_AT = float(os.environ.get('POSITION_MANAGMENT_SELL_AT', -2))
POSITION_MANAGENT_BUY_DAY_MINIMUM = float(os.environ.get('POSITION_MANAGENT_BUY_DAY_MINIMUM', 1))
POSITION_MANAGENT_BUY_ALL_TIME_MINIMUM = float(os.environ.get('POSITION_MANAGENT_BUY_ALL_TIME_MINIMUM', 5))
POSITION_MANAGENT_BUY_SINCE_LAST_ORDER = float(os.environ.get('POSITION_MANAGENT_BUY_SINCE_LAST_ORDER', 2))
POSITION_MANAGMENT_WAIT_TIME = float(os.environ.get('POSITION_MANAGMENT_WAIT_TIME', 60))
POSITION_MANAGMENT_BUY_SIZE_UP_PERCENTAGE = float(os.environ.get('POSITION_MANAGMENT_BUY_SIZE_UP_PERCENTAGE', 1))

def position_managment():
    while True:
        try:
            positions = get_all_positions()
            if positions:
                for position in positions:
                    print(position.symbol)
                    last_order = get_last_order_details(position.symbol)
                    if last_order:
                        manage_postion(position, last_order)

            time.sleep(POSITION_MANAGMENT_WAIT_TIME)  

        except Exception as error:
            print(error)


def manage_postion(position, last_order):

    try:
        wait_time = datetime.now(timezone.utc) - timedelta(hours=POSITION_MANAGENT_BUY_SINCE_LAST_ORDER) 

        last_order_date = last_order.filled_at
        if not last_order_date:
            return 
        
        add_stop_loss(position.symbol, position.qty)

        percentage_change = float(position.unrealized_plpc) * 100
        percentage_change_today = float(position.unrealized_intraday_plpc) * 100

        if (last_order_date < wait_time) and (percentage_change > POSITION_MANAGENT_BUY_ALL_TIME_MINIMUM) and (percentage_change_today > POSITION_MANAGENT_BUY_DAY_MINIMUM):
            value_to_buy = math.ceil((float(position.unrealized_intraday_plpc) * POSITION_MANAGMENT_BUY_SIZE_UP_PERCENTAGE ) * float(position.market_value))
            print("Buying ", position.symbol, " due to position managment")
            stock_value = get_asset_price(position.symbol)
            buyAmount = math.ceil(value_to_buy / stock_value)
            buy_stock(position.symbol, buyAmount)
        if (percentage_change < POSITION_MANAGMENT_SELL_AT) or (percentage_change_today < POSITION_MANAGMENT_SELL_AT):
            print("Selling all ", position.symbol, " due to position managment")
            sell_all_stock(position.symbol)

    except Exception as error:
        print(error)
