import time
import json
import pandas as pd
import random
# import requests # 方法一
import cloudscraper # 方法二(建立在requests之上)
# from urllib.request import Request, urlopen # 方法三

alldata = []
last_article = ''
url = 'https://www.dcard.tw/service/api/v2/forums/talk/posts?limit=30'
# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

## 方法二
scraper = cloudscraper.create_scraper()
for i in range(2):
    try:
        if i != 0:
            requests_url = url+'&before='+str(last_article)
        else:
            requests_url = url
        ## 方法一
        # last_req = requests.get(requests_url, headers=headers)
        # getdata = json.loads(last_req.content)
        
        ## 方法二
        last_req = scraper.get(requests_url)
        getdata = json.loads(last_req.content)
        
        ## 方法三
        # request_site = Request(requests_url, headers=headers)
        # getdata = urlopen(request_site).read()
        # getdata = json.loads(getdata)
        
        alldata.extend(getdata)
        last_article = getdata[-1]['id']
        print(last_article)
        time.sleep(random.uniform(20,30)) # 隨機浮點數; randint隨機整數
    # except Exception as e:
    #     print(e)
    except:
        print(last_req)
    
alldata = pd.DataFrame(alldata)
## 30筆存一份
# outputdata = pd.DataFrame(getdata)
## 每次額外加30筆
# outputdata = pd.DataFrame(alldata)
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
alldata.to_csv(
    './文章輸出結果-測試/Dcard文章資料test.csv',
    encoding='utf-8-sig',
    index=False
)
    # if i==0:
    #     outputdata.to_csv(
    #         'C:/Users/Victor/Desktop/大學專題/程式/爬蟲-Dcard/文章輸出結果-測試/Dcard文章前'+str(30*(i+1))+'筆資料.csv',
    #         encoding='utf-8-sig',
    #         index=False
    #     )
    # else:
    #     outputdata.to_csv(
    #         'C:/Users/Victor/Desktop/大學專題/程式/爬蟲-Dcard/文章輸出結果-測試/Dcard文章第'+str(30*i+1)+'筆至第'+str(30*(i+1))+'筆資料.csv',
    #         encoding='utf-8-sig',
    #         index=False
    #     )
