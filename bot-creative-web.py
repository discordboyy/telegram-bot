import os
import requests
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = '-1001997933600'
ETH_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
PRICE_FILE = "eth_price.txt"

def get_current_eth_price():
    try:
        resp = requests.get(ETH_API_URL)
        resp.raise_for_status()
        return resp.json()['ethereum']['usd']
    except Exception as e:
        print(f"[get_current_eth_price] Error fetching price: {e}")
        return None

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text}
    try:
        resp = requests.post(url, data=data)
        resp.raise_for_status()
        print("[send_message] Message sent successfully!")
    except Exception as e:
        print(f"[send_message] Failed to send message: {e}")

def load_previous_price():
    try:
        with open(PRICE_FILE, "r") as f:
            return float(f.read().strip())
    except FileNotFoundError:
        return None

def save_price(price):
    with open(PRICE_FILE, "w") as f:
        f.write(str(price))

@app.route("/")
def index():
    return "Bot is ready ✅"

if __name__ == "__main__":
    current_price = get_current_eth_price()
    if current_price is None:
        print("Failed to get current price, exiting.")
        exit(1)

    previous_price = load_previous_price()

    if previous_price is None:
        send_message(f"📊 First run. Current ETH price: ${current_price:.2f}")
    else:
        change = current_price - previous_price
        if previous_price == 0:
            percent = 0
        else:
            percent = (change / previous_price) * 100
        direction = "📈 Grown" if change > 0 else "📉 Fell" if change < 0 else "⏸ No change"
        message = (
            f"📊 ETH current price: ${current_price:.2f}\n"
            f"{direction}: {percent:.2f}% vs 24h ago"
        )
        send_message(message)

    save_price(current_price)

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
