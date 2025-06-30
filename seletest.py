import subprocess
import random
from playwright.sync_api import sync_playwright

# 김도성 020708 - 

def random_delay():
    delay = random.uniform(0.3, 0.8)
    return delay*100

insta_id = "---"
insta_pw = "helllo"


follower_list = []
follow_list = []

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

chrome_port = 1243

chrome_process = subprocess.Popen([
    chrome_path,
    f"--remote-debugging-port={chrome_port}",
    "--user-data-dir=C:/temp-chrome",
    "--disable-infobars",
    "--no-first-run",
    "--disable-popup-blocking",
    "--disable-gpu",
    "--disable-extensions",
    "--disable-software-rasterizer",
    "--start-maximized",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-client-side-phishing-detection",
    "--disable-hang-monitor",
    "--disable-prompt-on-repost",
    "--disable-sync",
    "--metrics-recording-only",
    "--password-store=basic",
    "--use-mock-keychain",
])


with sync_playwright() as playwright:
    browser = playwright.chromium.connect_over_cdp(f"http://localhost:{chrome_port}")

    context = browser.new_context()

    page = context.new_page()

    page.set_default_navigation_timeout(15000)
    page.set_default_timeout(15000)

    page.set_extra_http_headers({
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \";Not A Brand\";v=\"99\"",
    })

    page.goto("https://www.instagram.com/?flo=true")

    id_xpath = page.locator("xpath=/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[1]/div/label/input")
    pw_xpath = page.locator("xpath=/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[2]/div/label/input")
    login_xpath = page.locator("xpath=/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[3]/button/div")

    id_xpath.type(insta_id, delay=random_delay())
    pw_xpath.type(insta_pw, delay=random_delay())
    login_xpath.click(force=True)

    while True:

        try:
            page.wait_for_selector("xpath=/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div[8]/div/span/div/a/div", timeout=30000) # 로그인 성공 판단
            print("로그인 성공")
            break
        except:
            print("실패 - 계속 찾음")
            pass

    page.locator('text="프로필"').click(force=True)

    # 팔로워 목록 추출 -------------------------------------

    page.locator('text="팔로워"').click(force=True)
    print("팔로워 클릭")

    xpath_list = ["xpath=/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]",
                  "xpath=/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]",
                  "xpath=/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"]
    
    div_xpath = 0
    
    for xpath in xpath_list:
        try:
            page.wait_for_selector(xpath, timeout=3000)
            div_xpath = xpath
            div_num = xpath[21]
            break
        except:
            pass
    
    print(div_num)

    try:

        page.click(div_xpath)
        
        scroll_box = page.locator(f'xpath=/html/body/div[{div_num}]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')

        scroll_location = scroll_box.evaluate("el => el.scrollHeight")

        while True:
            scroll_box.evaluate("el => el.scrollTo(0, el.scrollHeight)")

            page.wait_for_timeout(3000)
            
            scroll_height = scroll_box.evaluate("el => el.scrollHeight")
            
            if scroll_location == scroll_height:
                break
            else:
                scroll_location = scroll_height

        print("scroll success")

    except:
        print("scroll error")

    possible_parent_xpaths = [
    '/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div',
    '/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div',
    '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div',
    ]

    found = False

    for xpath in possible_parent_xpaths:
        try:
    
            page.wait_for_selector(f'xpath={xpath}', timeout=3000)
            
            parent = page.locator(f'xpath={xpath}')
            children = parent.locator('xpath=./div')
            count = children.count()
            
            if count > 0:
                
                for i in range(count):
                    follower_div = children.nth(i)
                    
            
                    spans = follower_div.locator('xpath=.//span')
                    span_count = spans.count()
                    
                    for j in range(span_count):
                        text = spans.nth(j).inner_text().strip()
                        if text:
                            # print(f"{i+1}번째 팔로워 {text}")
                            follower_list.append(text)
                            break  
                found = True
                break
        except:
            continue

    if not found:
        print("Error 1")


    possible_close_xpath = ["xpath=/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button",
                            "xpath=/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button",
                            "xpath=/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button"]

    for xpath in possible_close_xpath:
        try:
            page.wait_for_selector(xpath, timeout=3000)
            page.click(xpath)
            #close
            break
        except:
            print("pass")

    # ------------------------------

    # 팔로잉 목록 추출 -------------------------------

    page.locator('text="팔로우"').click(force=True)
    print("팔로우 클릭")

    xpath_list = ["xpath=/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]",
                  "xpath=/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]",
                  "xpath=/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"]
    
    div_xpath = 0
    
    for xpath in xpath_list:
        try:
            page.wait_for_selector(xpath, timeout=3000)
            div_xpath = xpath
            div_num = xpath[21]
            break
        except:
            pass
    
    print(div_num)

    try:

        page.click(div_xpath)
        
        scroll_box = page.locator(f'xpath=/html/body/div[{div_num}]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')

        scroll_location = scroll_box.evaluate("el => el.scrollHeight")

        while True:
            scroll_box.evaluate("el => el.scrollTo(0, el.scrollHeight)")

            page.wait_for_timeout(3000)
            
            scroll_height = scroll_box.evaluate("el => el.scrollHeight")
            
            if scroll_location == scroll_height:
                break
            else:
                scroll_location = scroll_height

        print("scroll success")

    except:
        print("scroll error")

    possible_parent_xpaths = [
    '/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div',
    '/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div',
    '/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div',
    ]

    found = False

    for xpath in possible_parent_xpaths:
        try:
    
            page.wait_for_selector(f'xpath={xpath}', timeout=3000)
            
            parent = page.locator(f'xpath={xpath}')
            children = parent.locator('xpath=./div')
            count = children.count()
            
            if count > 0:
                
                for i in range(count):
                    follower_div = children.nth(i)
                    
            
                    spans = follower_div.locator('xpath=.//span')
                    span_count = spans.count()
                    
                    for j in range(span_count):
                        text = spans.nth(j).inner_text().strip()
                        if text:
                            # print(f"{i+1}번째 팔로우 : {text}")
                            follow_list.append(text)
                            break  
                found = True
                break
        except:
            continue

    if not found:
        print("Error 2")


    possible_close_xpath = ["xpath=/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button",
                            "xpath=/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button",
                            "xpath=/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button"]

    for xpath in possible_close_xpath:
        try:
            page.wait_for_selector(xpath, timeout=3000)
            page.click(xpath)
            #close
            break
        except:
            print("pass")

    print("팔로워 팔로잉 목록 수집")

    print(f"팔로워 {len(follower_list)}명")
    print(f"팔로잉 {len(follow_list)}명")
    print("비활성화 계정으로 인해 미세한 차이 발생 가능")

    only_i_follow = list(set(follow_list) - set(follower_list))
    print("나만 그 사람을 팔로우:", only_i_follow, f"{len(only_i_follow)}명")

    only_they_follow = list(set(follower_list) - set(follow_list))
    print("그 사람만 나를 팔로우:", only_they_follow, f"{len(only_they_follow)}명")

    input("엔터를 눌러서 종료하세요")

    page.close()
    browser.close()
    playwright.stop()
