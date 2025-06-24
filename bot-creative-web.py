import os
import requests

TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = '-1001997933600'  # your channel ID

def send_message(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHANNEL_ID, 'text': text}
    try:
        resp = requests.post(url, data=data, timeout=10)
        resp.raise_for_status()
        print(f"Message sent successfully: {text}")
    except Exception as e:
        print(f"Failed to send message: {e}")

if __name__ == '__main__':
    send_message("🤖 I'm alive!")
