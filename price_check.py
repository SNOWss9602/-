from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests

URL = "https://openai.com/chatgpt/pricing"
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

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)
    time.sleep(5)  # 렌더링 기다리기

    text = driver.find_element("tag name", "body").text
    driver.quit()

    print("💬 페이지에서 추출한 텍스트 일부:")
    print(text[:1000])  # 처음 1000자만 미리보기

    keywords = ["$20", "20 USD", "ChatGPT Plus", "Plus plan", "Upgrade to Plus", "USD", "per month"]
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


