from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    try:
        # ✅ XPath: 정확한 가격 요소를 기다림
        xpath = "//div[contains(@class, 'text-xl') and contains(text(), '$20')]"

        # ✅ 최대 30초 기다림 (동적 렌더링 보장)
        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )

        price = element.text
        driver.quit()
        return price
    except Exception as e:
        driver.quit()
        print(f"❌ 가격 정보를 찾지 못했습니다. {e}")
        return ""

def main():
    price = fetch_price()
    if price:
        send_telegram_message(f"✅ 현재 ChatGPT Plus 가격: {price}")
    else:
        send_telegram_message("⚠️ 가격 정보를 찾을 수 없습니다. 페이지 구조가 바뀌었거나 로딩이 안 됐을 수 있어요.")

if __name__ == "__main__":
    main()

