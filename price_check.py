import requests
from bs4 import BeautifulSoup
import os

URL = "https://openai.com/pricing"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    telegram_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(telegram_api, data=data)

def fetch_price():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n")
    
    # 더 유연한 키워드로 검색
    keywords = ["$20", "20 USD", "ChatGPT Plus", "subscribe", "subscription"]
    matched_lines = [line.strip() for line in text.splitlines() if any(kw in line for kw in keywords)]
    
    return "\n".join(matched_lines)

def main():
    current_price = fetch_price()
    if current_price:
        send_telegram_message(f"💡 ChatGPT Plus 가격 관련 정보:\n\n{current_price}")
    else:
        send_telegram_message("❗ ChatGPT Plus 가격 정보를 찾을 수 없었습니다. 웹페이지 구조가 바뀌었을 수도 있어요.")

if __name__ == "__main__":
    main()
