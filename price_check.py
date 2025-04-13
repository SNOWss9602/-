from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests

# 🎯 정확한 가격 페이지
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

    try:
        # ⏳ 'Plus' 텍스트가 나올 때까지 대기 (최대 10초)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Plus')]"))
        )
    except:
        print("❌ 타임아웃: 가격 정보가 로드되지 않았습니다.")

    page_text = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()

    # 🔍 관심 있는 키워드
    keywords = ["$20", "20 USD", "ChatGPT Plus", "Plus plan", "per month", "subscription", "Upgrade"]
    found = [kw for kw in keywords if kw in page_text]
    return "\n".join(found)

def main():
    try:
        price_info = fetch_price()
        if price_info:
            send_telegram_message(f"💰 ChatGPT 가격 정보 발견:\n\n{price_info}")
        else:
            send_telegram_message("📭 가격 정보를 찾을 수 없습니다. 페이지 구조가 바뀌었을 수 있어요.")
    except Exception as e:
        send_telegram_message(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    main()
