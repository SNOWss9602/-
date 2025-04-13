from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import requests

URL = "https://openai.com/chat"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    telegram_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(telegram_api, data=data)

def fetch_price():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    time.sleep(5)  # JS 로딩 기다리기 (더 필요하면 늘릴 수 있음)

    text = driver.page_source
    driver.quit()

    keywords = ["$20", "20 USD", "ChatGPT Plus", "subscription", "subscribe"]
    found = [kw for kw in keywords if kw in text]
    return "\n".join(found)

def main():
    try:
        price_info = fetch_price()
        if price_info:
            send_telegram_message(f"💡 ChatGPT Plus 가격 관련 키워드 발견:\n\n{price_info}")
        else:
            send_telegram_message("❗ 가격 관련 키워드를 찾을 수 없습니다.")
    except Exception as e:
        send_telegram_message(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    main()

