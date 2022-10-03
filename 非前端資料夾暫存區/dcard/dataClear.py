from pymongo import MongoClient
import jieba as jieba
import time
import requests
import json
import pandas as pd
import random
commentname = 'Dcard留言資料40至900筆資料'
postname = 'Dcard文章資料5'
clear = '_Clear'
csv = '.csv'
removeword = ['span', 'class', 'f3', 'https', 'imgur', 'h1', '_   blank', 'href', 'rel', 'nofollow', 'target', 'cdn', 'cgi', 'b4', 'jpg', 'hl', 'b1', 'f5', 'f4',
              'goo.gl', 'f2', 'email', 'map', 'f1', 'f6', '__cf___', 'data', 'bbs''html', 'cf', 'f0', 'b2', 'b3', 'b5', 'b6', '原文內容', '原文連結', '作者'
              '標題', '時間', '看板', '<', '>', '，', '。', '？', '—', '閒聊', '・', '/', ' ', '=', '\"', '\n', '」', '「', '！', '[', ']', '：', '‧', '╦', '╔', '╗', '║', '╠', '╬', '╬', ':', '╰', '╩', '╯', '╭', '╮', '│', '╪', '─', '《', '》', '.', '、', '（', '）', '　', '*', '※', '~', '○', '”', '“', '～', '@', '＋', '\r', '▁', ')', '(', '-', '═', '?', ',', '!', '…', '&', ';', '『', '』', '#', '＝', '＃', '\\', '\\n', '"', '的', '^', '︿', '＠', '$', '＄', '%', '％',
              '＆', '＊', '＿', '+', "'", '{', '}', '｛', '｝', '|', '｜', '．', '‵', '`', '；', '●', '§', '※', '○', '△', '▲', '◎', '☆', '★', '◇', '◆', '□', '■', '▽',
              '▼', '㊣', '↑', '↓', '←', '→', '↖', '【', '】'
              ]
jieba.set_dictionary('dict.txt.big')
jieba.load_userdict('user_dict.txt')


def postclean():

    dcard_data = pd.read_csv(postname+csv)

    dcard_data = dcard_data[['文章ID', '標題', '內文簡介', '版ID', '回應的文章ID',
                            '發文時間', '回覆數', '按讚數', '主題標籤', '版中文名', '回應的文章的標題', '媒體連結']]

    dcard_data = dcard_data.drop_duplicates()

    dcard_data.info()
    dcard_data['發文時間'] = pd.to_datetime(dcard_data['發文時間'])

    dcard_data['所有文'] = dcard_data['標題'] + dcard_data['內文簡介']

    for word in removeword:
        dcard_data['所有文'] = dcard_data['所有文'].str.replace(word, '')

    dcard_data = dcard_data.dropna(subset=["所有文"])
    dcard_data['關鍵字'] = dcard_data['所有文'].apply(lambda x: list(jieba.cut(x)))
    dcard_data.to_csv(postname+clear+csv,
                      encoding='UTF-8-sig')

# jieba.set_dictionary('dict.txt.big')
# jieba.load_userdict('user_dict.txt')
# dcard_data = dcard_data.dropna(subset=["所有文"])
# dcard_data['文章關鍵字'] = dcard_data['所有文'].apply(lambda x: list(jieba.cut(x)))
# dcard_data['留言關鍵字'] = dcard_data['所有文'].apply(lambda x: list(jieba.cut(x)))
# dcard_data.info()


def commentclean():
    dcard_coment_data = pd.read_csv(commentname+csv)
    dcard_coment_data = dcard_coment_data[[
        '文章ID', '發文時間', '更新時間', '留言內容', '按讚數']]
    dcard_coment_data = dcard_coment_data.drop_duplicates()
    dcard_coment_data['發文時間'] = pd.to_datetime(dcard_coment_data['發文時間'])
    for word in removeword:
        dcard_coment_data['留言內容'] = dcard_coment_data['留言內容'].str.replace(
            word, '')
    dcard_coment_data = dcard_coment_data.dropna(subset=["留言內容"])
    dcard_coment_data['關鍵字'] = dcard_coment_data['留言內容'].apply(
        lambda x: list(jieba.cut(x)))
    for y in dcard_coment_data.index:
        if len(dcard_coment_data.loc[y, '關鍵字']) < 2:
            dcard_coment_data = dcard_coment_data.drop([y])
    dcard_coment_data.to_csv(commentname+clear+csv,
                             encoding='UTF-8-sig')

    # 存檔csv
postclean()
