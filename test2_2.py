import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import platform


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

def user_login(uid,upw):
    parent = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR,'div.global-menu-sign-in-_-sign_in_wrapper')))
    login_btn = parent.find_element(By.CSS_SELECTOR, "button[type='button']")
    login_btn.click()
    email_btn= wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(normalize-space(),'이메일')]]")
            )
        )
    email_btn.click()
    email_box = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,"input[type='text']")
            )
        )
    email_box.send_keys(uid)
    pw_box = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,"input[type='password']")
            )
        )
    pw_box.send_keys(upw)
    ac_login_btn= wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(normalize-space(),'로그인')]]")
            )
        )
    ac_login_btn.click()

    try:
        code_box = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='text' and contains(@placeholder,'인증코드')]")
            )
        )
        mail_code = input('인증코드 : ')
        code_box.send_keys(mail_code)
        confirm_code = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(normalize-space(),'인증코드 확인')]]")
            )
        )
        confirm_code.click()

        popup_confirm = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(normalize-space(),'확인')]]")
            )
        )
        popup_confirm.click()

    except TimeoutException: # 로그인시 메일 인증을 안할시 pass (캐시 등 이유)
        pass

def join_comm(artist_name):
    comm = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(normalize-space(),'커뮤니티 찾기')]]")
        )
    )
    comm.click()
    find_artist = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,
            "//input[@type='text' and contains(@placeholder,'아티스트의 이름을 입력하세요.')]")
        )
    )
    find_artist.send_keys(f'{artist_name}')

    join = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(normalize-space(),'가입')]]")
        )
    )
    join.click()
    time.sleep(2)
    driver.refresh()

    parent = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'li.my-community-list-view-_-carousel_item')
        )
    )
    artist_comm = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//span[contains(normalize-space(),'{artist_name}')]")
        )
    )
    artist_comm.click()

    profile = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class,'global-header-profile') and contains(@class,'profile')]")
        )
    )
    profile.click()

########### 이제 포스트 작성
# 1. 텍스트 , 이미지 첨부 등록
# 2. 등록한 포스트 확인 (텍스트 이미지 확인)
# 3. 포스트 수정 (텍스트 교체 / 이미지 삭제-> 영상 교체)
# 4. 수정 확인
# 5. 포스트 삭제 후 포스트 없을때 메시지 확 (아직 작성한 포스트가 없습니다.)

def post():
    post_box = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'div.wev-editor-input-v3-_-text')
        )
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", post_box)
    driver.execute_script("arguments[0].click();", post_box)
    con_result = post_content()
    test_text = con_result[0]
    test_file_name = con_result[1]
    try:
        submit_locator = (By.XPATH, "//button[.//span[contains(normalize-space(),'등록')]]")
        submit_btn = wait.until(EC.presence_of_element_located(submit_locator))

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)

        hide_btn_state = post_hide()

        wait.until(EC.element_to_be_clickable(submit_locator))
        driver.execute_script("arguments[0].click();", submit_btn)

    except (NoSuchElementException, TimeoutException) as e:
        print("hide/등록 처리 중 오류:", e)
        hide_btn_state = None

    return hide_btn_state, test_text, test_file_name

def post_content():
    post_edit = wait.until(
        EC.element_to_be_clickable(
            (By.ID, 'wev-editor')
        )
    )
    # 텍스트 등록
    edit_text = input('포스트 글 내용 입력 :')
    post_edit.click()
    post_edit.send_keys(edit_text)


    while True:
        try:
            which_file = input('첨부 파일 선택 (이미지[i] / 영상[v] ) :')

            # 이미지 등록
            if which_file.lower() == 'i':
                upload_image = wait.until(
                    EC.presence_of_element_located(
                        (By.ID,'weuii')
                    )
                )
                upload_image.send_keys('/Users/seunghwanlee/Desktop/image_list/min1.jpeg')
                confirm_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH,"//button[contains(normalize-space(),'확인')]")
                    )
                )
                confirm_btn.click()
                img_name = 'min1'
                return edit_text,img_name
            # 영상
            elif which_file.lower() == 'v':
                upload_video = wait.until(
                    EC.presence_of_element_located(
                        (By.ID,'weuvi')
                    )
                )
                upload_video.send_keys('/Users/seunghwanlee/Desktop/video_list/vid1.mp4')
                confirm_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(normalize-space(),'확인')]")
                    )
                )
                confirm_btn.click()
                vid_name = 'vid1'
                return edit_text,vid_name
            else :
                print('입력값 오류')
        except (NoSuchElementException, TimeoutException) as e:
            print('요소 찾기 불가 / 클릭 대기 중 에러 :', e)

def post_hide():
    hide_aria = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@role='checkbox']")
        )
    )
    hide_state = hide_aria.get_attribute('aria-checked').lower() == 'true'
    if hide_state:
        hide_result = 'ON'
        return hide_result
    # 아티스트에게 테스트가 되도록이면 노출되지 않도록
    else:
        hide_btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[.//span[contains(normalize-space(),'Hide from')]]")
            )
        )
        hide_btn.click()
        hide_result = 'ON'
        return hide_result

def post_edit():
    more_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(normalize-space(),'more')]]")
        )
    )
    more_btn.click()

    edit_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(normalize-space(),'수정')]]")
        )
    )
    edit_btn.click()

    editor_text = wait.until(EC.element_to_be_clickable((By.ID, "wev-editor")))
    editor_text.click()

    if platform.system() == "Darwin":
        editor_text.send_keys(Keys.COMMAND, "a")
    else:
        editor_text.send_keys(Keys.CONTROL, "a")

    # 삭제
    editor_text.send_keys(Keys.BACK_SPACE)

    # 새 글 입력
    new_text = input('수정 할 텍스트 : ')
    editor_text.send_keys(new_text)
    notMean = 'null'

    while True:
        try:
            which_file = input('첨부 파일 선택 (이미지[i] / 영상[v] ) :')

            # 이미지 등록
            if which_file.lower() == 'i':
                upload_image = wait.until(
                    EC.presence_of_element_located(
                        (By.ID,'weuii')
                    )
                )
                upload_image.send_keys('/Users/seunghwanlee/Desktop/image_list/min1.jpeg')
                confirm_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH,"//button[contains(normalize-space(),'확인')]")
                    )
                )
                confirm_btn.click()
                img_name = 'min2'
                return notMean,new_text,img_name
            # 영상
            elif which_file.lower() == 'v':
                upload_video = wait.until(
                    EC.presence_of_element_located(
                        (By.ID,'weuvi')
                    )
                )
                upload_video.send_keys('/Users/seunghwanlee/Desktop/video_list/vid1.mp4')
                confirm_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(normalize-space(),'확인')]")
                    )
                )
                confirm_btn.click()
                vid_name = 'vid1'
                return notMean,new_text,vid_name
            else :
                print('입력값 오류')
        except (NoSuchElementException, TimeoutException) as e:
            print('요소 찾기 불가 / 클릭 대기 중 에러 :', e)

def post_delete():
    time.sleep(5)
    more_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(normalize-space(),'more')]]")
        )
    )
    more_btn.click()

    delete_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(normalize-space(),'삭제')]]")
        )
    )
    delete_btn.click()

    delete_confirm_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(normalize-space(),'확인')]]")
        )
    )
    delete_confirm_btn.click()

    try:
        toast = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(@class,'Toast-_-label')]"))
        )
        print(toast.text)

        if "삭제" in toast.text:
            print("삭제 성공 토스트 확인")
        else:
            print("삭제 토스트 내용 불일치")

    except TimeoutException:
        print("삭제 토스트 미노출")


user_id = input('아이디 입력 : ')
user_pw = input('패스워드 입력 : ')
user_login(user_id,user_pw)
artist = input('커뮤 카입할 아티스트 :')
join_comm(artist)
result = post()
########################################### 등록 검증 ################################################################
text_locator = wait.until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            f"//div[contains(@class,'line-clamp-node-view')]/div[contains(normalize-space(), '{result[1]}')]"
        )
    )
)
post_text = text_locator.text


img_locator = driver.find_element(By.XPATH, "//div[contains(@class,'post-module-_-image_wrap')]//img")

img_src = img_locator.get_attribute("src")

if result[1] in post_text:
    print('포스트 텍스트 자동 입력 성공')
else:
    print('자동화 실패')

if result[2] in img_src:
    print('포스트 사진 자동 입력 성공')
else:
    print('자동화 실패')
####################################################################################################################
after_result = post_edit()

submit_locator = (By.XPATH, "//button[.//span[contains(normalize-space(),'등록')]]")
submit_btn = wait.until(EC.presence_of_element_located(submit_locator))

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)

wait.until(EC.element_to_be_clickable(submit_locator))
driver.execute_script("arguments[0].click();", submit_btn)

post_delete()
