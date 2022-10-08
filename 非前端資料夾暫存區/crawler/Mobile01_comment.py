import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup
import random
import time
from pymongo import MongoClient
import json
import re
from Mobile01_title import title


title_page = 2
most_comment_page = 20

# url = 'https://www.mobile01.com/topicdetail.php?f=37&t=6081707'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
getdata = {"title": [], "content": [], "keypoint": [], "time": []}
commentdata = {"title": [], "name": [], "comment": [], "time": []}
allpostdata = []
allcommentdata = []
    
def database_connection():
    try:
        conn = MongoClient(host='localhost', port=27017)
        db = conn['Data']
        collection = db['Mobile01']
        # collection = db['Testing']
        print("Connecting Successful")
    except:
        print("Fail to connect to 'mongodb://localhost:27017/'")
    
    # read_data = collection.find()
    # read_data = title()
    # print(read_data['href'])
    
    # for record in read_data['href'][:2]:
    #     print(record)
    # url = record['href']
    return collection

def comment(urls):
    for url in urls:
        last_page = 0
        i = 1
        keypoint = []
    
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
            if pages.text == []:
                last_page = 1
        # print("包含留言共", last_page, "頁")
    
        for a_tag in soup.find_all(class_="o-hashtag u-gapTop--sm"):
            keyword = a_tag.text
            keyword = keyword.replace('\n', '')
            keypoint.append(keyword)
        # print("文章關鍵字：", keypoint)
        getdata['keypoint'].append(keypoint)
        
        crawl_time = soup.find(class_=re.compile("o-fNotes o-fSubMini")).text
        getdata['time'].append(crawl_time)
    
        print(getdata)
        time.sleep(random.uniform(5,10))
    
        # while i <= 2:  # 強制限定頁數
        while (i <= int(last_page)) & (i <= most_comment_page):
            article_ignore = 1
            try:
                if i > 1:
                    request_url = url + '&p=' + str(i)
                else:
                    request_url = url  # 第一次執行，不須加上後方的before
                resp = scraper.get(request_url, headers=headers)
                soup = BeautifulSoup(resp.text, 'html.parser')
    
                print("-----", i, "-----")
                for a_tag in soup.find_all(class_="l-articlePage")[article_ignore:]:
                    commentdata['title'].append(crawl_title)
                    
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
                    
                    try:
                        time_tag = a_tag.find_all(class_=re.compile("o-fNotes o-fSubMini"))[0]
                        times = pd.to_datetime(time_tag.text)
                    except IndexError:
                        times=pd.to_datetime(crawl_time)
                    except:
                        time_tag = a_tag.find_all(class_=re.compile("o-fNotes o-fSubMini"))[1]
                        times = pd.to_datetime(time_tag.text)
                    commentdata['time'].append(times)
                    print("留言時間：", times)
                    print()
                i += 1
                time.sleep(random.uniform(5, 15))
            except Exception as e:
                print('Error: ', e)
                print('Error happened at Page ', i, ' !!')
                time.sleep(random.uniform(30, 45))
        time.sleep(random.uniform(10,15))
        
    allpostdata = pd.DataFrame(getdata)
    # allpostdata.columns = ['標題', '內文', '關鍵字']
    print(allpostdata)

    print()
    allcommentdata = pd.DataFrame(commentdata)
    # allcommentdata.columns = ['標題', '留言名字', '回覆內容']
    print(allcommentdata)
    
    passdata = {'allpostdata': allpostdata, 'allcommentdata': allcommentdata}
    print(passdata)
    
    return passdata

if __name__ == '__main__':
    data = title(title_page)
    alldata = comment(data['href'])
    allpostdata = pd.DataFrame(alldata['allpostdata'])
    allcommentdata = pd.DataFrame(alldata['allcommentdata'])
    
    db_collection = database_connection()
    tInsert = db_collection.insert_many(json.loads(allpostdata.T.to_json()).values())
    cInsert = db_collection.insert_many(json.loads(allcommentdata.T.to_json()).values())
    
    

