from alpacaHandler import buy_stock, sell_all_stock, get_asset
from openAIHandler import send_to_openai 
from prompts import get_news_review, header_prompt
import os
import json

def new_news(current_event):
    company_impact = 0
    if len(current_event['symbols']) != 1:
        return
    
    ticker_symbol = current_event['symbols'][0]


    asset = get_asset(ticker_symbol)

    if asset.fractionable == False:
        return
      

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

    print(ticker_symbol, company_impact)
    if company_impact >= 100:
        buy_stock(ticker_symbol, 20, json_string)
    elif company_impact >= 90:
        buy_stock(ticker_symbol, 10, json_string)
    elif company_impact >= 80:
        buy_stock(ticker_symbol, 5, json_string)
    elif company_impact <= -50:
        sell_all_stock(ticker_symbol)
