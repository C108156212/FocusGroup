# using flask_restful
from flask import Flask, jsonify, request, render_template
import json
from flask_restful import Resource, Api
import datetime
from pymongo import MongoClient
import pandas as pd
from ToJson_26 import run_jsonifier
# TCSA 是分析情緒分數的核心，可以呼叫兩個函數：
#   Degree: 傳入一段文字語料，回傳情緒評極。評極範圍 0.00 ~ 10.0
#   Orientation: 傳入一段文字語料，回傳情緒判斷結果。「Positive」「Negative」

# Step1: 準備一個名為 Data 的資料庫（database）（Data這個命名可改）

# Step2: 準備一個名為 Dcard 的資料表（collection）（Dcard這個命名可改）

# Step3: 建立 nosql 連線
client = MongoClient(
    host="mongodb+srv://Crawler_admin:Crawling15622@cluster0.sc0f7sr.mongodb.net/?retryWrites=true&w=majority", port=5000)
db = client['Data']
collection = db.Original_Data
# 只篩選留言的欄位 暫定欄位名稱為 "comment"
# table = collection.find({}, {'所有文': True})

# collection.find({},{"word":True}) 查詢結果篩選 word 欄位
# collection.find({},{"value":False}) 查詢結果排除 value 欄位
# collection.find({"name":"Jone"})  查詢結果篩選 [name=Jone] 的資料
# collection.find({},{"value":{$gt:60}})  #查詢 value 大於60的資料
# collection.findOne() 查詢下一筆資料
# collection.find().sort({"column":1}) column 欄位遞增排序(1)、遞減排序(0)
# collection.find().count() 回傳資料筆數
# collection.find().limit(100) 回傳前100筆查詢結果

# Step4: 迴圈讀取範例


x = datetime.datetime.now()
# creating the flask app
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# creating an API object
api = Api(app)


class PLOT1(Resource):
    def get(self, p1, p2, p3, p4, p5):
        postfilter = {"$or": [{"content": {'$regex': p1}},
                      {"content": {'$regex': p2}}, {"content": {'$regex': p5}}, {"content": {'$regex': p3}}, {"content": {'$regex': p4}}]}
        commentfilter = {"$or": [{"comment": {'$regex': p1}}, {"comment": {'$regex': p2}}, {
            "comment": {'$regex': p3}}, {"comment": {'$regex': p4}}, {"comment": {'$regex': p5}}]}
        posttags = collection.find(postfilter)
        commenttags = collection.find(commentfilter)
        # print(posttags)

        pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None)
        products = [p1, p2, p3, p4, p5]

        postdata = []
        commentdata = []
        postdata = pd.DataFrame(posttags)
        commentdata = pd.DataFrame(commenttags)
        print(postdata)
        print(commentdata)

        # ---------------------文章整合----------------------------
        postdata['time'] = pd.to_datetime(postdata['time'])
        postdata['time'] = postdata['time'].apply(
            lambda x: x.strftime('%Y-%m-%d')).values
        posttags = postdata.groupby(by=['time', 'site', 'title']).sum()
        populartags_post = str(postdata['content'].sum())
        # print(posttags)

        # ---------------------留言整合---------------------------------
        commentdata['time'] = pd.to_datetime(commentdata['time'])
        commentdata['time'] = commentdata['time'].apply(
            lambda x: x.strftime('%Y-%m-%d')).values
        commenttags = commentdata.groupby(by=['time', 'site', 'title']).sum()
        populartags_comment = str(commentdata['comment'].sum())
        print(commenttags)

        # ------------文章標籤聲量整合-------------------
        post_voice = []
        popular_voice = []

        comment_voice = []
        for m in products:
            voice = populartags_post.count(m)
            post_voice.append(voice)
        # print(post_voice)

        post_voice_df = pd.DataFrame(zip(products, post_voice))
        post_voice_df.columns = ["文章標籤名稱", "文章聲量"]
        # print('post_voice_df:', post_voice_df)
        post_voice_df = post_voice_df.sort_values(by=["文章聲量"], ascending=False)
        print("post_voice_df:", post_voice_df)

        # -------------留言標籤聲量整合-------------------
        for m in products:
            voice = populartags_comment.count(m)
            comment_voice.append(voice)

        comment_voice_df = pd.DataFrame(zip(products, comment_voice))
        comment_voice_df.columns = ["留言標籤名稱", "留言聲量"]
        # print('comment_voice_df:', comment_voice_df)
        comment_voice_df = comment_voice_df.sort_values(
            by=["留言聲量"], ascending=False)
        # print("comment_voice_df:", comment_voice_df)

        # ---------------文章時間來源ID標籤聲量整合-------------------
        allpost_voice = []
        for i in post_voice_df['文章標籤名稱']:
            # print(i)
            post_tags = []
            for m in posttags['content']:
                voice3 = m.count(i)
                post_tags.append(voice3)
            allpost_voice.append(post_tags)
        print("allpost_voice", allpost_voice)

        allpost_voice_df = pd.DataFrame(map(list, zip(*allpost_voice)))
        allpost_voice_df.columns = post_voice_df['文章標籤名稱']
        allpost_voice_df.index = posttags.index
        allpost_voice_df.reset_index(inplace=True)

        # print("allpost_voice_df_type:", type(allpost_voice_df))
        # ---------------留言時間來源ID標籤聲量整合-------------------
        allcomment_voice = []
        for i in comment_voice_df['留言標籤名稱']:
            # print(i)
            tags = []
            for m in commenttags['comment']:
                voice3 = m.count(i)
                tags.append(voice3)
            allcomment_voice.append(tags)

        allcomment_voice_df = pd.DataFrame(map(list, zip(*allcomment_voice)))
        allcomment_voice_df.columns = comment_voice_df['留言標籤名稱']
        allcomment_voice_df.index = commenttags.index
        allcomment_voice_df.reset_index(inplace=True)

        # ---------------------------輸出文章json檔----------------------
        with open('post.json', 'w', encoding='utf-8-sig') as file:
            allpost_voice_df.to_json(file, force_ascii=False)
        # print('done')
        # 顯示品牌聲量繪折線圖

        f = open("post.json", encoding="utf-8-sig")
        data = json.loads(f.read())
        json_post = json.dumps(data, ensure_ascii=False)
        # -------------------------輸出留言json檔---------------------------
        with open('comment.json', 'w', encoding='utf-8-sig') as file:
            allcomment_voice_df.to_json(file, force_ascii=False)
        # print('done')
        # 顯示品牌聲量繪折線圖

        f = open("comment.json", encoding="utf-8-sig")
        data = json.loads(f.read())
        json_comment = json.dumps(data, ensure_ascii=False)
        return jsonify({"文章": json_post, "留言": json_comment})


# adding the defined resources along with their corresponding urls
# api.add_resource(Hello, '/api')
# api.add_resource(Square, '/api/square/<int:num>')
# api.add_resource(Data, '/api/data')
# api.add_resource(TCSA1, '/api/TCSA1/<int:num>')
api.add_resource(
    PLOT1, '/api/home/<string:p1>/<string:p2>/<string:p3>/<string:p4>/<string:p5>')


# driver function
if __name__ == '__main__':

    app.run(debug=True)
