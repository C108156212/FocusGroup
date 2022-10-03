from playwright.sync_api import sync_playwright
import pandas as pd
import random
import logging
import time
allpostdata = []
allcommentdata = []
logger = logging.getLogger()
last_page = 0
with sync_playwright() as p:
    getdata = {"title": [], "content": [], "keypoint": []}
    commentdata = {"name": [], "comment": []}
    keypoint = []
    i = 1
    url = 'https://www.mobile01.com/topicdetail.php?f=37&t=6081707'
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    # page.query_selector("[class='t2']")
    print("標題：", end='')
    print(page.query_selector("[class='t2']").text_content())
    getdata['title'].append(page.query_selector("[class='t2']").text_content())
    print("內文：", end='')
    print(page.query_selector("[itemprop='articleBody']").text_content())
    getdata['content'].append(page.query_selector(
        "[itemprop='articleBody']").text_content())
    for a_tag in page.query_selector_all("[class='l-pagination__page ']"):
        last_page = a_tag.text_content()
    for a_tag in page.query_selector_all("[class='l-input__item']"):
        print("文章關鍵字：", end='')
        print(a_tag.text_content())
        keypoint.append(a_tag.text_content())
    getdata['keypoint'].append(a_tag.text_content())
    browser.close()
    while i <= int(last_page):
        try:
            if i > 1:  # 判斷是否是第一次執行
                request_url = url + '&p=' + str(i)
            else:
                request_url = url  # 第一次執行，不須加上後方的before
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(request_url)

            for a_tag in page.query_selector_all("[class='c-authorInfo__id']"):
                print("留言名字：", end='')
                print(a_tag.text_content())
                commentdata['name'].append(a_tag.text_content())
            for a_tag in page.query_selector_all("article"):
                print("回覆內容", end='')
                print(a_tag.text_content())
                commentdata['comment'].append(a_tag.text_content())
            print("--------------------")
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
    allpostdata = pd.DataFrame(getdata)
    allpostdata.columns = ['標題', '內文', '關鍵字']
    print(allpostdata)
    print(commentdata)
    allcommentdata = pd.DataFrame(commentdata)
    allcommentdata.columns = ['留言名字', '回覆內容']
    print(allcommentdata)
    allpostdata.to_csv(
        './mobile01文章內容test.csv',
        encoding='utf-8-sig',
        index=False
    )
    allcommentdata.to_csv(
        './mobile01留言內容test.csv',
        encoding='utf-8-sig',
        index=False
    )
