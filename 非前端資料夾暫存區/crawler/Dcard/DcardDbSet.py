# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 02:01:43 2022

@author: Victor
"""

from pymongo import MongoClient
from mongoclean import MongoClean


def Dbset():
    try:
        # conn = MongoClient(
        #     host='localhost', port=27017)
        # db = conn['Data']
        # collection = db['Dcard02']

        conn = MongoClient(
            host='mongodb+srv://Crawler_admin:Crawling15622@cluster0.sc0f7sr.mongodb.net/?retryWrites=true&w=majority', port=5000)
        db = conn['Data']
        collection = db['Original_Data']
        # collection = db['Testing']
        print("Connecting Successful")
    except:
        print("Fail to connect to 'mongodb://localhost:27017/'")

    list1 = []
    cleanwords = ['[', ']', '\'', ' ']
    # 找出存在"tag"標籤的資料
    for data in collection.find({'tag': {'$exists': True}, 'site': "Dcard"}):
        tags = data['tag']
        if type(tags) == str:
            for cleaner in cleanwords:
                tags = tags.replace(cleaner, "")

            if tags == "":
                tag = list(tags)
            else:
                tag = tags.split(",")
            collection.update_one({'_id': data['_id']}, {'$set': {'tag': tag}})
        else:
            print("tag不是字串")
    print("dbsetdone")
    MongoClean()


Dbset()
