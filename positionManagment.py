
from alpacaHandler import get_all_positions, get_last_order_details, buy_stock, sell_all_stock
import time
from datetime import datetime, timedelta, timezone
import math


def position_managment(): 
    positions = get_all_positions()
    if positions:
        for position in positions:
            last_order = get_last_order_details(position.symbol)
            if last_order:
                manage_postion(position, last_order)

    time.sleep(600) # Wait 10 minuites then manage positions again
    position_managment()


def manage_postion(position, last_order):

    time_24_hours_ago = datetime.now(timezone.utc) - timedelta(hours=24) 

    last_order_date = last_order.filled_at

    percentage_change = float(position.unrealized_plpc) * 100
    percentage_change_today = float(position.unrealized_intraday_plpc) * 100

    if (last_order_date < time_24_hours_ago) and (percentage_change > 5) and (percentage_change_today > 0):
        value_to_buy = math.ceil(float(position.unrealized_intraday_plpc) * float(position.market_value))
        print("Buying stock due to position managment")
        buy_stock(position.symbol, value_to_buy)
            
    if (percentage_change < -5) or (percentage_change_today < -5):
        print("Selling stock due to position managment")
        sell_all_stock(position.symbol)

# position OBJ 
# {  
#     'asset_class': 'us_equity',
#     'asset_id': 'f801f835-bfe6-4a9d-a6b1-ccbb84bfd75f',
#     'asset_marginable': True,
#     'avg_entry_price': '174.728',
#     'change_today': '0',
#     'cost_basis': '4.999999849',
#     'current_price': '174.45',
#     'exchange': 'NASDAQ',
#     'lastday_price': '174.45',
#     'market_value': '4.99204462725',
#     'qty': '0.028615905',
#     'qty_available': '0.028615905',
#     'side': 'long',
#     'symbol': 'AMZN',
#     'unrealized_intraday_pl': '-0.00795522159', - amount
#     'unrealized_intraday_plpc': '-0.0015910443661005',   - percent
#     'unrealized_pl': '-0.00795522175',
#     'unrealized_plpc': '-0.0015910443980495'
# }
        


# order OBJ
# {   
#     'asset_class': 'us_equity',
#     'asset_id': '230eb69c-58ed-4fcf-a5e8-540db323d34c',
#     'canceled_at': None,
#     'client_order_id': '{"rating": 80, "newsId": 37041780}',
#     'created_at': '2024-02-09T19:21:31.654137Z',
#     'expired_at': None,
#     'extended_hours': False,
#     'failed_at': None,
#     'filled_at': '2024-02-09T19:21:31.658218Z',
#     'filled_avg_price': '109.206',
#     'filled_qty': '0.04578503',
#     'hwm': None,
#     'id': '515bafa0-657c-4daf-8eb4-359f195c3e8b',
#     'legs': None,
#     'limit_price': None,
#     'notional': '5',
#     'order_class': '',
#     'order_type': 'market',
#     'qty': None,
#     'replaced_at': None,
#     'replaced_by': None,
#     'replaces': None,
#     'side': 'buy',
#     'source': 'access_key',
#     'status': 'filled',
#     'stop_price': None,
#     'submitted_at': '2024-02-09T19:21:31.652961Z',
#     'subtag': None,
#     'symbol': 'NET',
#     'time_in_force': 'day',
#     'trail_percent': None,
#     'trail_price': None,
#     'type': 'market',
#     'updated_at': '2024-02-09T19:21:31.659971Z'
# }