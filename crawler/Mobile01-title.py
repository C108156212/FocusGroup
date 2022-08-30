# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 15:10:15 2022

@author: Victor
"""

import cloudscraper
from bs4 import BeautifulSoup
import time
import random

scraper = cloudscraper.create_scraper()
url = 'https://www.mobile01.com/forumtopic.php?c=35'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

for page in range(2):
    resp = scraper.get(url+"&p="+str(page+1), headers=headers)
    print("\n第", page+1, "頁")
    print("Status: ", resp.status_code)
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
    
        ## 篩選標籤
        # t_tags = soup.select("div.c-listTableTd__title a") ##1.(No)
        # t_tags = soup.find("div", class_="c-listTableTd__title").find("a").text ##2.(No)
        for a_tag in soup.find_all("div", class_="c-listTableTd__title"):
            print("標題：", end='')
            print(a_tag.find("a").text) ##3.(ok)
        # for t in t_tags: ##1
        #     print(t.text)
    else:
        print("沒找到東西QQ")
    
    time.sleep(random.uniform(5,10))
