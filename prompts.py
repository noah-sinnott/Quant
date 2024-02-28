header_prompt = "Only respond with a number from -100 to 100 detailing the impact of the news story. Do not respond with anything but a number"

def get_news_review(h, s, ticker):
    return f"Given the stock {ticker}, headline '{h}', and summary ${s} show me a number from -100 to 100 detailing the impact of the news story with -100 being that the story will strongly negativly imapct the stock, 0 being it will have no impact on the stock and 100 being a strong positive impact. If ypu need more info reply 0"