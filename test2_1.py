import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests


def weverse(id,pw):
    parent = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,'div.global-menu-sign-in-_-sign_in_wrapper')
        )
    )
    login_btn = parent.find_element(By.CSS_SELECTOR, "button[type='button']")
    login_btn.click()

    new_account = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[normalize-space()='회원가입']")
        )
    )
    new_account.click()

    email_btn = wait.until(
        EC.element_to_be_clickable((
            (By.XPATH, "//button[.//span[contains(normalize-space(),'이메일')]]")
        ))
    )
    email_btn.click()

    ###여기까지가 이멜로 회원가입 누르기

    email_box = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,"input[type='email']")
        )
    )
    email_box.send_keys(id)

    pw_box = driver.find_elements(
        By.CSS_SELECTOR,"input[type='password']"
    )
    pw_box[0].send_keys(pw)
    pw_box[1].send_keys(pw)

    code_response_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,"//button[.//span[contains(normalize-space(),'인증코드')]]")
        )
    )
    code_response_btn.click()

    code_box = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@type='text' and contains(@placeholder,'인증코드')]"
             )
        )
    )
    mail_code = input('메일의 인증코드 입력 : ')
    code_box.send_keys(mail_code)
    ## 인증코드 받기 / 인증코드 확인하는 btn의 class명이 동일하여 한번 더 체크해서 찾음
    code_confirm_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(normalize-space(),'인증코드')]]")
        )
    )
    code_confirm_btn.click()
    # 다음
    next_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,"//button[.//span[contains(normalize-space(),'다음')]]")
        )
    )
    next_btn.click()

    agree_btn = wait.until(
        EC.presence_of_element_located(
            (By.XPATH,"//button[.//span[contains(normalize-space(),'모두') and contains(normalize-space(),'동의')]]")
        )
    )
    agree_btn.click()

    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    accession_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,"//button[.//span[contains(normalize-space(),'가입하기')]]")
        )
    )
    accession_btn.click()

    confirm_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,"//button[.//span[contains(normalize-space(),'확인')]]")
        )
    )
    confirm_btn.click()
    start_btn= wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(normalize-space(),'시작')]]")
        )
    )
    start_btn.click()

def find_token(driver, target_url):
    logs = driver.get_log("performance")

    for entry in reversed(logs):
        msg = json.loads(entry["message"])["message"]
        if msg.get("method") != "Network.requestWillBeSent":
            continue

        req = msg.get("params", {}).get("request", {})
        url = req.get("url", "")
        headers = req.get("headers", {})

        if target_url in url and "Authorization" in headers:
            return headers["Authorization"], url

    return None, None


options = webdriver.ChromeOptions()

prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
}

options.add_experimental_option("detach", True)
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("prefs", prefs)
options.add_argument("--disable-notifications")
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

driver.get('https://weverse.io')

################### 중복 가입이 안되기 때문에, 해당 부분 변경 필요 ###################
id = 'winerik0421@gmail.com'
pw = 'h2112626@!'
###########################################################################
target_url = 'https://global.apis.naver.com/weverse/wevweb/users/v1.0/users/me'

weverse(id,pw)

driver.refresh()
time.sleep(2)

auth, real_url = find_token(driver, target_url)
print("AUTH:", auth)
print("REAL URL:", real_url)


if not auth or not real_url:
    print("토근 발견 못함")
else:
    headers = {
        "Authorization": auth,
        "Referer": "https://weverse.io/"
    }

    r = requests.get(real_url, headers=headers)
    print("STATUS:", r.status_code)
    data = r.json()
    wid = data["wid"]
    print("id :",id,"\nPW :",pw,"\nwid :",wid)

driver.quit()