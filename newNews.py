from alpacaHandler import buy_stock, sell_all_stock
from openAIHandler import send_to_openai 
from prompts import get_news_review, header_prompt
import os

async def new_news(current_event):
    company_impact = 0

    api_request_body = {
        "model": os.environ.get("OPEN_AI_VERSION"),
        "messages": [
            {"role": "system", "content": header_prompt},
            {"role": "user", "content": get_news_review(current_event['headline'])}
        ]
    }

    temp = await send_to_openai(api_request_body)
    if not temp:
        return

    company_impact = int(temp)

    ticker_symbol = current_event['symbols'][0]

    if company_impact >= 70:
        buy_stock(ticker_symbol, 1)
    elif company_impact <= 30:
        sell_all_stock(ticker_symbol)
