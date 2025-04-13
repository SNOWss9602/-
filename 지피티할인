import requests
from bs4 import BeautifulSoup
import os

URL = "https://openai.com/chat"
PRICE_KEYWORD = "ChatGPT Plus"

TELEGRAM_TOKEN = os.getenv("8171814256:AAGyBN1eLwbZS1l-9qkAxCW9VN294mTyGkw")
CHAT_ID = os.getenv("-4606998554")

def send_telegram_message(message):
    telegram_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(telegram_api, data=data)

def fetch_price():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if PRICE_KEYWORD in line]
    return "\n".join(lines)

def main():
    current_price = fetch_price()
    if current_price:
        send_telegram_message(f"💡 ChatGPT Plus 가격 정보:\n\n{current_price}")
    else:
        send_telegram_message("❗ 가격 정보를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
