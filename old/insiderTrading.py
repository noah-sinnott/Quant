
from alpacaHandler import get_all_positions, get_last_order_details, buy_stock, sell_all_stock
import time
import datetime
import requests



def get_latest_insider_trades(): 


    url = "https://api.unusualwhales.com/api/congress/recent-reports" + "?date=" datetime.date()

    headers = {
        "Accept": "application/json, text/plain",
        "Authorization": "Bearer 123"
    }

    response = requests.get(url, headers=headers)

    print(response.json())


    time.sleep(3600) # Wait 1 hour then get trades again
    get_latest_insider_trades()


def review_trade(trade):
    print(trade)