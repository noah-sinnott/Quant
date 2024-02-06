import json
import os
from websocket import create_connection, WebSocketApp
from newNews import new_news 
from dotenv import load_dotenv
import os

load_dotenv()  

def on_open(ws):
    print("Websocket connected!")
    auth_msg = json.dumps({
        "action": "auth",
        "key": os.environ['APCA_API_KEY_ID'],
        "secret": os.environ['APCA_API_SECRET_KEY']
    })
    ws.send(auth_msg)
    subscribe_msg = json.dumps({
        "action": "subscribe",
        "news": ["*"]
    })
    ws.send(subscribe_msg)

def on_message(ws, message):
    current_event = json.loads(message)[0]
    if current_event.get("T") == "n":
        newNews(current_event)  # Assuming newNews is adapted to handle Python dictionaries

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("### closed ###")

if __name__ == "__main__":
    ws_url = "wss://stream.data.alpaca.markets/v1beta1/news"
    ws = WebSocketApp(ws_url,
                      on_open=on_open,
                      on_message=on_message,
                      on_error=on_error,
                      on_close=on_close)
    ws.run_forever()
