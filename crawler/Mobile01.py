from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd
import random
import logging
import time


def run():
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.mobile01.com/forumtopic.php?c=35
    page.goto("https://www.mobile01.com/login.php?link=%2Fforumtopic.php%3Fc%3D35")

    # Click header div:has-text("登入/註冊") >> nth=4

    # Click input[name="regEmail"]
    page.locator("input[name=\"regEmail\"]").click()

    # Fill input[name="regEmail"]
    page.locator("input[name=\"regEmail\"]").fill("victorfion@gmail.com")

    # Press Tab
    page.locator("input[name=\"regEmail\"]").press("Tab")

    # Fill input[name="regPassword"]
    page.locator("input[name=\"regPassword\"]").fill("victor88")

    # Click button:has-text("登入")
    page.locator("button:has-text(\"登入\")").click()

    # ---------------------
    page.wait_for_load_state("networkidle")
    context.storage_state(path='./state.json')
    browser.close()


with sync_playwright() as playwright:
    run()


def title():
    alldata = []
    logger = logging.getLogger()
    with sync_playwright() as p:
        i = 1
        getdata = {"title": [], "herf": []}
        while i <= 1:
            try:
                url = 'https://www.mobile01.com/forumtopic.php?c=35&sort=topictime'
                if i > 0:  # 判斷是否是第一次執行
                    request_url = url + '&p=' + str(i)
                else:
                    request_url = url  # 第一次執行，不須加上後方的before

                browser = p.chromium.launch(headless=False)
                context = browser.new_context(storage_state='./state.json')
                page = context.new_page()
                page.goto(request_url)
                for a_tag in page.query_selector_all("[class='c-link u-ellipsis']"):
                    print("標題：", end='')
                    print(a_tag.text_content())
                    getdata['title'].append(a_tag.text_content())
                    print("網址：", end='')
                    print('https://www.mobile01.com/' +
                          a_tag.get_attribute('href'))
                    getdata['herf'].append('https://www.mobile01.com/' +
                                           a_tag.get_attribute('href'))
                    # titledata.append(a_tag.text_content())
                print("###########")
                browser.close()
                i += 1
                time.sleep(random.uniform(20, 40))
            except Exception as e:
                logger.exception(
                    'Exception occurred while code execution: ' + str(e))
                print('!!!!!!!!!!'+url+'!!!!!!!!!!!!!!!!!')

                if str(e) == 'HTTP Error 404: Not Found':
                    doit = False
                print(i)
                time.sleep(random.uniform(60, 180))
                browser.close()

        alldata = pd.DataFrame(getdata)
        alldata.columns = ['標題', '網址']
        print(alldata)
        # for a_tag in page.query_selector_all("[class='c-listTableTd__title']"):
        #     print("網址：")
        #     print(a_tag.text_content())  # 3.(ok)
        # print(titledata)

        alldata.to_csv(
            './mobile01文章資料test.csv',
            encoding='utf-8-sig',
            index=False
        )


title()
