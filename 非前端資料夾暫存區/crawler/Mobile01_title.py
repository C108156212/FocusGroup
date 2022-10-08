# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 15:10:15 2022

@author: Victor
"""

import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
# from pymongo import MongoClient
# import json


scraper = cloudscraper.create_scraper()
url = 'https://www.mobile01.com/forumtopic.php?c=35'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

getdata = {"title": [], "href": [], "time":[]}
alldata = []

def title(pages):
    for page in range(int(pages)):
        try:
            resp = scraper.get(url+"&p="+str(page+1), headers=headers)
            print("\n第", page+1, "頁")
            print("Status: ", resp.status_code)

            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")

                # 篩選標籤
                # t_tags = soup.select("div.c-listTableTd__title a") ##1.(No)
                # t_tags = soup.find("div", class_="c-listTableTd__title").find("a").text ##2.(No)
                for a_tag in soup.find_all("div", class_="c-listTableTd__title"):
                    title = a_tag.find("a").text  # 3.(ok)
                    print("標題：", title)
                    getdata['title'].append(title)
                    href = 'https://www.mobile01.com/' + a_tag.a.get("href")
                    print("網址：", href)
                    getdata['href'].append(href)
                for a_tag in soup.find_all("div", class_="o-fNotes")[::2]:
                    times = a_tag.text
                    # print("發佈時間：", times)
                    getdata['time'].append(times)
                # for t in t_tags: ##1
                #     print(t.text)
            else:
                print("錯誤：", resp.status_code)
        except Exception as e:
            print("Error:", e)

        time.sleep(random.uniform(5, 10))

    alldata = pd.DataFrame(getdata)
    # alldata.columns = ["標題", "網址", "發佈時間"]
    print(alldata)
    return alldata


    # # conn = MongoClient('mongodb://localhost:27017/')
    # conn = MongoClient(host='localhost', port=27017)
    # db = conn['Data']  # 創建資料庫
    # # db = conn.Data
    # collection = db['Mobile01']  # 創建資料表
    # print(collection.stats)  # 確認連線狀態

    # # 存入資料庫
    # insert = collection.insert_many(json.loads(alldata.T.to_json()).values())
    # # print(insert.inserted_id)

    # print("Collection(documents)總數：", collection.count_documents({}))

    # =====================
    # 讀取資料
    # read = collection.find()
    # for record in read:
    #     print(record)

    # 刪除資料
    # collection.delete_one({"title": "給分功能真正的意義"})
    # # 全部刪除delete = collection.delete_many({})


