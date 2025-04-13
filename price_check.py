from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests

# URL 및 Telegram 설정
URL = "https://openai.com/chatgpt/pricing"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    telegram_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(telegram_api, data=data)

def fetch_price():
    # Chrome Headless 설정
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)

    try:
        # XPath에 해당하는 요소가 로드될 때까지 최대 20초 대기
        xpath = "//div[contains(@class, 'text-xl') and contains(text(), '$20')]"
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        price_text = element.text
        driver.quit()
        return price_text
    except Exception as e:
        driver.quit()
        print("❌ 가격 정보를 찾지 못했습니다.", e)
        return ""

def main():
    try:
        price = fetch_price()
        if price:
            send_telegram_message(f"✅ 현재 ChatGPT Plus 가격: {price}")
        else:
            send_telegram_message("⚠️ 가격 정보를 찾을 수 없습니다. 페이지 구조가 바뀌었을 수 있어요.")
    except Exception as e:
        send_telegram_message(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    main()


