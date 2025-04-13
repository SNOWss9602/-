from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
import tempfile

# 🎯 정확한 가격 페이지 URL
URL = "https://openai.com/chatgpt/pricing"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    telegram_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(telegram_api, data=data)

def fetch_price():
    options = Options()
    # 임시 디렉토리로 user-data-dir을 설정하여 충돌을 방지
    user_data_dir = tempfile.mkdtemp()  # 임시 디렉토리 생성
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)

    try:
        # 페이지에서 가격 정보가 나타날 때까지 대기 (최대 60초)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/main/div[1]/section[1]/div/div/div[1]/div/div/div[2]/div[3]/ul/li/span[2]"))
        )
    except Exception as e:
        print(f"❌ 타임아웃: 가격 정보가 로드되지 않았습니다. 에러: {e}")
        driver.quit()
        return ""

    # 정확한 XPath를 사용하여 가격 정보 추출
    try:
        # 가격 정보를 포함하는 요소 찾기
        price_elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div[3]/div[1]/main/div[1]/section[1]/div/div/div[1]/div/div/div[2]/div[3]/ul/li/span[2]")
        prices = [element.text for element in price_elements]
        driver.quit()

        return "\n".join(prices)

    except Exception as e:
        print(f"❌ 가격 정보를 찾는 중 에러 발생: {e}")
        driver.quit()
        return ""

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


