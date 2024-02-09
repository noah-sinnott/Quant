from openai import OpenAI
import os

client = OpenAI()

def send_to_openai(body):
    try:
        response = client.chat.completions.create( 
            model=os.environ.get("OPEN_AI_VERSION"),
            messages=body
            )
        
        if response:
            return response.choices[0].message.content
        else:
            return False
    except Exception as e:
        print(f"error sending to open ai: {e}")
        return False
