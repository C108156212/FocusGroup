# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 15:46:48 2022

@author: Victor
"""

import pandas as pd
from glob import glob
from pymongo import MongoClient
import json


files = glob("C:/Users/Victor/Documents/GitHub/FocusGroup/非前端資料夾暫存區/data/Dcard文章資料*.csv")
df = pd.concat((pd.read_csv(file) for file in files), ignore_index=True)
df.drop_duplicates(subset="文章ID", inplace=True)

files_comment = glob("C:/Users/Victor/Documents/GitHub/FocusGroup/非前端資料夾暫存區/data/Dcard留言資料*.csv")
df_comment = pd.concat((pd.read_csv(file) for file in files_comment), ignore_index=True)
df_comment.drop_duplicates(subset="留言內容", inplace=True)


df = df[["文章ID", "所有文", "主題標籤", "發文時間"]]
df.rename(columns={
    '文章ID': 'title',
    '所有文': 'content',
    '主題標籤': 'tag',
    '發文時間': 'time',
        }, inplace=True)
print(df)
print()
df_comment = df_comment[["文章ID", "發文ID", "留言內容", "發文時間"]]
df_comment.rename(columns={
    '文章ID': 'title',
    '發文ID': 'name',
    '留言內容': 'comment',
    '發文時間': 'time',
        }, inplace=True)
print(df_comment)

conn = MongoClient(host='localhost', port=27017)
db = conn['Data']
collection = db['Dcard']
print(collection.stats)

tInsert = collection.insert_many(json.loads(df.T.to_json()).values())
cInsert = collection.insert_many(json.loads(df_comment.T.to_json()).values())

