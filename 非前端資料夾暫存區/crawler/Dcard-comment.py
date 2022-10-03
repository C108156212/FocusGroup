import time
import json
import pandas as pd
import random
# import requests # 方法一
import cloudscraper # 方法二(建立在requests之上)
# from urllib.request import Request, urlopen # 方法三

dcard_article = pd.read_csv('./文章輸出結果-測試/Dcard文章資料.csv')
# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

scraper = cloudscraper.create_scraper(delay=10)
stop=False
alldata = []
for articleID in dcard_article['文章ID']:
    url = 'https://www.dcard.tw/service/api/v2/posts/' + \
        str(articleID) + '/comments'
    last_comment = 0
    i = 0
    while True:
        try:
            if i != 0:
                request_url = url + '?after=' + str(last_comment)
            else:
                request_url = url
            # last_req = requests.get(request_url, headers=headers)
            # getdata = json.loads(last_req.content)
            
            last_req = scraper.get(request_url)
            getdata = json.loads(last_req.content)
            
            # request_site = Request(request_url, headers=headers)
            # getdata = urlopen(request_site).read()
            # getdata = json.loads(getdata)
            print(i)
            print(request_url)
            if len(getdata) == 4:
                break
            elif len(getdata) > 0:
                alldata.extend(getdata)
                last_comment += len(getdata)
                i = i+1
                time.sleep(random.uniform(30,35))
            else:
                break
        except KeyboardInterrupt:
            stop=True
            print('KeyboardInterrupt')
            break
        # except Exception as e:
        #     print(e)
        #     time.sleep(random.randint(2,5))
        except:
            time.sleep(random.randint(60,90))
            print(last_req)
            # print(getdata)
    if stop == True:
        break
    time.sleep(random.randint(40,45))

alldata = pd.DataFrame(alldata)
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

alldata.to_csv(
    './留言輸出結果-測試/Dcard留言資料.csv',
    encoding='utf-8-sig',
    index=False
)
