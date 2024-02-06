import os
import requests

def send_to_openai(body):
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
                "Content-Type": "application/json"
            },
            json=body  # In requests, you can use the json parameter to automatically encode your dictionary to JSON
        )
        if response and response.ok:
            jsoned = response.json()
            return jsoned['choices'][0]['message']['content']
        else:
            return False
    except Exception as e:
        print(f"error sending to open ai: {e}")
        return False
