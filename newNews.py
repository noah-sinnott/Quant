from alpacaHandler import buy_stock, sell_all_stock, get_account_balance, get_asset_price
from openAIHandler import send_to_openai 
from prompts import get_news_review, header_prompt
import json
import math
import os

def new_news(current_event):



    company_impact = 0

    if len(current_event['symbols']) != 1:
        return
    
    ticker_symbol = current_event['symbols'][0]

    api_request_body = [
            {"role": "system", "content": header_prompt},
            {"role": "user", "content": get_news_review(current_event["headline"], current_event["summary"], ticker_symbol)}
        ]

    temp = send_to_openai(api_request_body)
    
    if not temp:
        return

    company_impact = int(temp)
    
    reasoning = {
        "rating": company_impact,
        "newsId": current_event["id"]
    }
    json_string = json.dumps(reasoning)
    print("News Item Found: ", ticker_symbol, " : ", company_impact)

    
    NEWS_BUY_AT = json.loads(os.environ.get('NEWS_BUY_AT', '{}'))
    NEWS_SELL_AT = json.loads(os.environ.get('NEWS_SELL_AT', '{}'))
    NEWS_SELL_ALL_AT = float(os.environ.get('NEWS_SELL_ALL_AT', '-50'))


    buyKeys = sorted(map(int, NEWS_BUY_AT.keys()), reverse=True)
    for key in buyKeys:
        if company_impact >= key:        
            cash = get_account_balance()
            value_to_buy = NEWS_BUY_AT[str(key)] * float(cash)
            stock_value = get_asset_price(ticker_symbol)
            buyAmount = math.ceil(value_to_buy / stock_value)
            buy_stock(ticker_symbol, buyAmount, json_string)
            return

    if company_impact <= NEWS_SELL_ALL_AT:
        sell_all_stock(ticker_symbol)


