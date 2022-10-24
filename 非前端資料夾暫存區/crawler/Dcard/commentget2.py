from playwright.sync_api import sync_playwright
import json
import time
import pandas as pd
import random
import logging

from dataClear import postclean


def Commentget():
    logger = logging.getLogger()
    dcard_article = pd.read_csv('Dcard文章資料.csv')
    alldata = []
    number = 0
    start = 0
    with sync_playwright() as p:
        for x in dcard_article.iloc:
            x['文章ID'].astype('int')
            number += 1
            if x['回覆數'] > 0:

                last_comment = 0
                url = 'https://www.dcard.tw/service/api/v2/posts/' + \
                    str(x['文章ID']) + '/comments'

                doit = True
                i = 0
                while doit:
                    time.sleep(random.uniform(10, 20))
                    try:
                        if i != 0:
                            request_url = url + '?after=' + str(last_comment)
                        else:
                            request_url = url
                        browser_type = p.webkit
                        browser = browser_type.launch(headless=False)
                        page = browser.new_page()
                        page.set_default_timeout(0)
                        page.goto(request_url)
                        if page.title == 'Just a moment...':
                            print('wait a moment')
                            page.wait_for_timeout(100)
                            if page.locator("text=Verify you are human") == True:
                                page.locator(
                                    "text=Verify you are human").click()
                            # page.locator("text=Verify you are human").click()
                            page.wait_for_url(
                                request_url)
                            getdata = json.loads(
                                page.text_content(selector='body'))
                            if len(getdata) == 4:
                                doit = False
                            elif len(getdata) > 0:
                                alldata.extend(getdata)
                                if len(getdata) == 30:
                                    last_comment += len(getdata)
                                    i = i+1
                                else:
                                    doit = False
                            else:
                                doit = False
                            print(request_url)
                            print(i)
                            time.sleep(random.uniform(10, 20))
                            browser.close()
                        else:
                            # page.locator("text=Verify you are human").click()
                            # print(json.loads(page.text_content(selector='body')))
                            page.wait_for_url(
                                request_url)
                            getdata = json.loads(
                                page.text_content(selector='body'))
                            if len(getdata) == 4:
                                doit = False
                            elif len(getdata) > 0:
                                alldata.extend(getdata)
                                if len(getdata) == 30:
                                    last_comment += len(getdata)
                                    i = i+1
                                else:
                                    doit = False
                            else:
                                doit = False
                            print(request_url)
                            print(i)
                            time.sleep(random.uniform(10, 20))
                            browser.close()
                    except Exception as e:
                        logger.exception(
                            'Exception occurred while code execution: ' + str(e))
                        print('!!!!!!!!!!'+url+'!!!!!!!!!!!!!!!!!')
                        time.sleep(random.uniform(10, 20))
                        page.reload()
                        page.frames
                        page.wait_for_load_state('domcontentloaded')
                        page.wait_for_url(
                            request_url)
                        if page.title() == 'Just a moment...':
                            human = False
                            print('wait a moment')
                            page.goto(request_url)
                            page.wait_for_timeout(8000)
                            n = 1
                            while human == False | n == 3:
                                if page.title() == 'Just a moment...':
                                    page.goto(request_url)
                                    page.wait_for_timeout(8000)
                                    # page.reload()
                                    # page.frames
                                    # page.wait_for_load_state(
                                    #     'domcontentloaded')
                                    page.wait_for_url(
                                        request_url)

                                    print(request_url)
                                    print(i)
                                    print('human=', human)
                                    n += 1
                                else:
                                    # page.reload()
                                    # page.frames
                                    page.wait_for_timeout(8000)
                                    page.wait_for_url(
                                        request_url)
                                    getdata = json.loads(
                                        page.text_content(selector='body'))
                                    if len(getdata) == 4:
                                        doit = False
                                    elif len(getdata) > 0:
                                        alldata.extend(getdata)
                                        if len(getdata) == 30:
                                            last_comment += len(getdata)
                                            i = i+1
                                        else:
                                            doit = False
                                    human = True
                                    print('human=', human)
                        else:
                            print('wait')
                            print(page.title())
                            # time.sleep(random.uniform(10, 20))
                            page.wait_for_url(
                                request_url)
                            getdata = json.loads(
                                page.text_content(selector='body'))
                            if len(getdata) == 4:
                                doit = False
                            elif len(getdata) > 0:
                                alldata.extend(getdata)
                                if len(getdata) == 30:
                                    last_comment += len(getdata)
                                    i = i+1
                                else:
                                    doit = False
                            else:
                                doit = False
                            print(request_url)
                            print(i)
                            time.sleep(random.uniform(10, 20))
                            browser.close()
                        if str(e) == 'HTTP Error 404: Not Found':
                            doit = False
                        time.sleep(random.uniform(10, 20))
                        browser.close()
                    print(f'number={number}')
            else:
                print(type(x['文章ID']))
                print(x['回覆數'])
    alldata = pd.DataFrame(alldata)
    # 翻譯欄位
    alldata.rename(columns={
        'id': '發文ID',
        'anonymous': '',
        'postId': '文章ID',
        'createdAt': '發文時間',
        'updatedAt': '更新時間',
        'floor': '樓層',
        'content': '留言內容',
        'likeCount': '按讚數',
        'hiddenByAuthor': '是否被作者隱藏',
        'gender': '性別',
        'school': '學校',
        'host': '是否為發文者',
        'hidden': '是否隱藏',
        'department': '個人主頁',
    }, inplace=True)
    # 存檔
    alldata.to_csv(
        'Dcard留言資料.csv',  # 檔案名稱
        encoding='utf-8-sig',  # 編碼
        index=False  # 是否保留index
    )
    print('已存檔')
    start = number
    print(f'start={start}')
    # browser.close()
    print("commentgetdone")
    postclean()


Commentget()
