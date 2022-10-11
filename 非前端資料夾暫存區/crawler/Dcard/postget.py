from pymongo import MongoClient
import jieba as jieba
import time

import json
import pandas as pd
import random

import random
import logging
from playwright.sync_api import sync_playwright
# https://www.dcard.tw/service/api/v2/forums/talk/posts?popular=true&limit=30&before=235999153
q = 16

logger = logging.getLogger()
with sync_playwright() as p:
    last_article = ''
    for d in range(5):
        alldata = []
        i = 0
        while i <= 5:
            try:
                url = 'https://www.dcard.tw/service/api/v2/forums/talk/posts?limit=30'
                if i > 0 or d > 0:  # 判斷是否是第一次執行
                    request_url = url + '&before=' + str(last_article)
                else:
                    request_url = url  # 第一次執行，不須加上後方的before
                print(i, d)
                browser_type = p.chromium
                browser = browser_type.launch(headless=False)
                page = browser.new_page()
                page.goto(request_url)  # 請求
                # list_req.add_header('User-Agent', random.choice(my_headers))
                # 將整個網站的程式碼爬下來
                getdata = json.loads(page.text_content(selector='body'))
                alldata.extend(getdata)  # 將另一個陣列插在最後面
                last_article = getdata[-1]['id']  # 取出最後一篇文章
                print(last_article)
                i = i+1
                time.sleep(random.uniform(30, 50))
                print('done')
                browser.close()
            except Exception as e:
                logger.exception(
                    'Exception occurred while code execution: ' + str(e))
                print('!!!!!!!!!!'+url+'!!!!!!!!!!!!!!!!!')

                if str(e) == 'HTTP Error 404: Not Found':
                    doit = False
                print(i)
                time.sleep(random.uniform(60, 180))
                browser.close()

        alldata = pd.DataFrame(alldata)
        # 翻譯欄位
        alldata.rename(columns={
            'id': '文章ID',
            'title': '標題',
            'excerpt': '內文簡介',
            'anonymousSchool': '學校匿名',
            'anonymousDepartment': '個人主頁顯示',
            'forumId': '版ID',
            'replyId': '回應的文章ID',
            'createdAt': '發文時間',
            'updatedAt': '更新時間',
            'commentCount': '回覆數',
            'likeCount': '按讚數',
            'topics': '主題標籤',
            'forumName': '版中文名',
            'forumAlias': '版英文名',
            'gender': '作者性別',
            'school': '作者學校',
            'replyTitle': '回應的文章的標題',
            'layout': '頁面版型',
            'withImages': '是否使用圖片',
            'withVideos': '是否使用影片',
            'media': '媒體連結',
            'department': '個人主頁',
            'categories': '類別',
            'link': '連結（版型為連結才有）'
        }, inplace=True)
        # 存檔
        alldata.to_csv(
            'Dcard文章資料'+str(int(q)+int(d))+'.csv',  # 檔案名稱
            encoding='utf-8-sig',  # 編碼
            index=False  # 是否保留index
        )

        dcard_data = pd.read_csv('Dcard文章資料'+str(int(q)+int(d))+'.csv')
        dcard_data = dcard_data[['文章ID', '標題', '內文簡介', '版ID', '回應的文章ID',
                                '發文時間', '回覆數', '按讚數', '主題標籤', '版中文名', '回應的文章的標題', '媒體連結']]
        dcard_data = dcard_data.drop_duplicates()
        dcard_data.info()
        dcard_data['發文時間'] = pd.to_datetime(dcard_data['發文時間'])
        dcard_data.info()
        dcard_data['所有文'] = dcard_data['標題'] + dcard_data['內文簡介']
        removeword = ['span', 'class', 'f3', 'https', 'imgur', 'h1', '_   blank', 'href', 'rel', 'nofollow', 'target', 'cdn', 'cgi', 'b4', 'jpg', 'hl', 'b1', 'f5', 'f4',
                      'goo.gl', 'f2', 'email', 'map', 'f1', 'f6', '__cf___', 'data', 'bbs''html', 'cf', 'f0', 'b2', 'b3', 'b5', 'b6', '原文內容', '原文連結', '作者'
                      '標題', '時間', '看板', '<', '>', '，', '。', '？', '—', '閒聊', '・', '/', ' ', '=', '\"', '\n', '」', '「', '！', '[', ']', '：', '‧', '╦', '╔', '╗', '║', '╠', '╬', '╬', ':', '╰', '╩', '╯', '╭', '╮', '│', '╪', '─', '《', '》', '.', '、', '（', '）', '　', '*', '※', '~', '○', '”', '“', '～', '@', '＋', '\r', '▁', ')', '(', '-', '═', '?', ',', '!', '…', '&', ';', '『', '』', '#', '＝', '＃', '\\', '\\n', '"', '的', '^', '︿', '＠', '$', '＄', '%', '％',
                      '＆', '＊', '＿', '+', "'", '{', '}', '｛', '｝', '|', '｜', '．', '‵', '`', '；', '●', '§', '※', '○', '△', '▲', '◎', '☆', '★', '◇', '◆', '□', '■', '▽',
                      '▼', '㊣', '↑', '↓', '←', '→', '↖', '【', '】'
                      ]
        for word in removeword:
            dcard_data['所有文'] = dcard_data['所有文'].str.replace(word, '')

        jieba.set_dictionary('dict.txt.big')
        jieba.load_userdict('user_dict.txt')
        dcard_data = dcard_data.dropna(subset=["所有文"])
        dcard_data['關鍵字'] = dcard_data['所有文'].apply(
            lambda x: list(jieba.cut(x)))
        dcard_data.info()

        dcard_data.to_csv('Dcard文章資料'+str(int(q)+int(d))+'_Clear.csv',
                          encoding='UTF-8-sig')
        time.sleep(random.uniform(30, 60))

# 存檔MongoDB


# client = MongoClient(host='localhost', port=27017)  # 连接mongodb端口

# db = client.Test
# crowd = db.data  # crowd表格

# # 将dataframe格式的user_review插入到crowd中
# crowd.insert_many(json.loads(dcard_data.T.to_json()).values())
