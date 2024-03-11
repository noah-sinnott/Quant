import json
import os
import threading
import sys
from dotenv import load_dotenv

def load_environment():
    if "--production" in sys.argv:
        load_dotenv('.env.production')
    else:
        load_dotenv()

load_environment()

from websocket import WebSocketApp
from newNews import new_news 
from positionManagment import position_managment

def on_news_ws_open(ws):
    print("News Websocket connected!")
    auth_msg = json.dumps({
        "action": "auth",
        "key": os.environ['APCA_API_KEY_ID'],
        "secret": os.environ['APCA_API_SECRET_KEY']
    })
    ws.send(auth_msg)
    subscribe_msg = json.dumps({
        "action": "subscribe",
        "news": ["*"],
    })
    ws.send(subscribe_msg)

def on_news_message(ws, message):
    messages = json.loads(message)
    for current_event in messages:
        if current_event.get("T") == "n":
            new_news(current_event) 


def on_error(ws, error):
    print(f"Error  : {error}")

def on_close(ws, close_status_code, close_reason):
    print("### closed ###")
    print(f"Close Status Code: {close_status_code}")
    print(f"Close Reason: {close_reason}")



def run_news_ws():
    news_ws_url = "wss://stream.data.alpaca.markets/v1beta1/news"
    news_ws = WebSocketApp(news_ws_url,
                           on_open=on_news_ws_open,
                           on_message=on_news_message,
                           on_error=on_error,
                           on_close=on_close)
    news_ws.run_forever()


if __name__ == "__main__":
    # position_managment()
    # run_news_ws()

    # initialise_meta_trader_5()

    news_thread = threading.Thread(target=run_news_ws,daemon=True)
    position_thread = threading.Thread(target=position_managment,daemon=True)
    
    news_thread.start()
    position_thread.start()

    news_thread.join()
    position_thread.join()
