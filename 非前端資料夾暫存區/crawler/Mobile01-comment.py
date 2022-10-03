import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup
import random
import time
from pymongo import MongoClient
import json


try:
    conn = MongoClient(host='localhost', port=27017)
    db = conn['Data']
    # collection = db['Mobile01']
    collection = db['Testing']
    print("Connecting Successful")
except:
    print("Fail to connect to 'mongodb://localhost:27017/'")

read_data = collection.find()
for record in read_data[:2]:
    print(record['href'])

    url = record['href']
    # url = 'https://www.mobile01.com/topicdetail.php?f=37&t=6081707'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

    last_page = 0
    i = 1
    article_ignore = 1
    getdata = {"title": [], "content": [], "keypoint": []}
    commentdata = {"name": [], "comment": []}
    keypoint = []
    allpostdata = []
    allcommentdata = []

    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url, headers=headers)

    soup = BeautifulSoup(resp.text, 'html.parser')

    crawl_title = soup.find("h1", class_="t2").text
    # print("標題：", crawl_title)
    getdata['title'].append(crawl_title)

    crawl_content = soup.find("div", itemprop="articleBody").text
    # print("內文：", crawl_content)
    getdata['content'].append(crawl_content)

    for pages in soup.find(class_="l-navigation__item--min").find_all(class_='l-pagination__page'):
        if pages.text != "":
            last_page = pages.text
    # print("包含留言共", last_page, "頁")

    for a_tag in soup.find_all(class_="o-hashtag u-gapTop--sm"):
        keyword = a_tag.text
        keyword = keyword.replace('\n', '')
        keypoint.append(keyword)
    # print("文章關鍵字：", keypoint)
    getdata['keypoint'].append(keypoint)

    print(getdata)
    time.sleep(random.uniform(5,10))

    while i <= 2:  # 強制限定頁數
        # while i <= int(last_page):
        try:
            if i > 1:
                request_url = url + '&p=' + str(i)
            else:
                request_url = url  # 第一次執行，不須加上後方的before
            resp = scraper.get(request_url, headers=headers)
            soup = BeautifulSoup(resp.text, 'html.parser')

            print("-----", i, "-----")
            for a_tag in soup.find_all(class_="l-articlePage")[article_ignore:]:
                name_tag = a_tag.find(class_="c-authorInfo__id")
                name_tag = name_tag.text.replace('\n', '')
                print("留言名字：", name_tag)
                commentdata['name'].append(name_tag)
                
                try:
                    comment_tag = a_tag.find("article", class_="u-gapBottom--max")
                    while True:
                        try:
                            comment_tag.blockquote.extract()
                        except:
                            break
                    comment_tag = comment_tag.text.replace('\n', '')
                except:
                    print("Tag not found !!")
                    article_ignore += 1
                print("回覆內容：", comment_tag)
                commentdata['comment'].append(comment_tag)
                print()
            i += 1
            time.sleep(random.uniform(10, 15))
        except Exception as e:
            print('Error: ', e)
            print('Error happened at Page ', i, ' !!')
            time.sleep(random.uniform(30, 45))


    allpostdata = pd.DataFrame(getdata)
    # allpostdata.columns = ['標題', '內文', '關鍵字']
    print(allpostdata)

    print()
    commentdata['title'] = [crawl_title]*len(commentdata['name'])
    allcommentdata = pd.DataFrame(commentdata)
    # allcommentdata.columns = ['標題', '留言名字', '回覆內容']
    print(allcommentdata)
    
    time.sleep(random.uniform(10,15))
    
    tInsert = collection.insert_many(json.loads(allpostdata.T.to_json()).values())
    cInsert = collection.insert_many(json.loads(allcommentdata.T.to_json()).values())
