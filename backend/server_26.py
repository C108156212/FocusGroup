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

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.


# class Hello(Resource):

#     # corresponds to the GET request.
#     # this function is called whenever there
#     # is a GET request for this resource
#     def get(self):

#         return jsonify({'message': 'hello world'})

#     # Corresponds to POST request
#     def post(self):

#         data = request.get_json()     # status code
#         return jsonify({'data': data}), 201


# another resource to calculate the square of a number
# class Square(Resource):

#     def get(self, num):

#         return jsonify({'square': num**2})


# class Data(Resource):

#     def get(self):

#         return jsonify({
#             'Name': "我是誰",
#             "Age": "22",
#             "Date": x,
#             "programming": "python"
#         })


# class TCSA1(Resource):
#     def get(self, num):
#         while True:
#             n = int(num)
#             data = table[n]['所有文']
#             return jsonify({
#                 "content": data,
#                 "rating": str(TCSA.Degree(data)),
#                 "emotional": TCSA.Orientation(data),
#             })


class PLOT1(Resource):
    def get(self, p1, p2, p3, p4, p5):
        tabletags = collection.find({'content': {"$ne": None}}, {
            'tag': 1, 'time': 1, 'site': 1})
        # products內放使用者產品
        p1 = str(p1)
        p2 = str(p2)
        p3 = str(p3)
        p4 = str(p4)
        p5 = str(p5)
        products = [p1, p2, p3, p4, p5]

        alldata = []
        alldata = pd.DataFrame(tabletags)
        alldata['time'] = pd.to_datetime(alldata['time'])
        alldata['time'] = alldata['time'].apply(
            lambda x: x.strftime('%Y-%m-%d')).values
        alltags = alldata.groupby(by=['time', 'site']).sum()
        # 暫定從tag中抓取
        populartags = str(alldata['tag'].sum())
        # print(alltags)
        products_voice = []
        popular_voice = []
        top3_voice = []

        for m in products:
            voice = populartags.count(m)
            products_voice.append(voice)

        brand_voice_df = pd.DataFrame(zip(products, products_voice))
        brand_voice_df.columns = ["time", "hot"]
        brand_voice_df = brand_voice_df.sort_values(
            by=["hot"], ascending=False)
        # populartag = brand_voice_df['time'].max()
        alltag = brand_voice_df['time'].head(5)
        # print('populartag:', populartag)
        # for i in alltags['tag']:
        #     # print(i)
        #     voice = i.count(populartag)
        #     popular_voice.append(voice)
        # print(popular_voice)

        for i in alltag:
            # print(i)
            tags = []
            for m in alltags['tag']:
                voice3 = m.count(i)
                tags.append(voice3)
            top3_voice.append(tags)

        # 最熱產品時間+產品名稱+聲量
        # pt_voice_df = pd.DataFrame(zip(alltags.index, popular_voice))
        # pt_voice_df.columns = ["time", populartag]
        # pt_voice_df[["time", "site"]] = pt_voice_df["time"].apply(pd.Series)
        # 前三熱產品時間+產品名稱+聲量
        top3_voice_df = pd.DataFrame(map(list, zip(*top3_voice)))
        top3_voice_df.columns = alltag
        top3_voice_df.index = alltags.index
        top3_voice_df.reset_index(inplace=True)
        # json_data = top3_voice_df.to_json()
        # top3_voice_df = top3_voice_df.to_dict()
        with open('df.json', 'w', encoding='utf-8-sig') as file:
            top3_voice_df.to_json(file, force_ascii=False)
        # print('done')
        # 顯示品牌聲量繪折線圖

        f = open("df.json", encoding="utf-8-sig")
        data = json.loads(f.read())
        json_str = json.dumps(data, ensure_ascii=False)

        # f = open("dcard_api_post_food.json", encoding="utf-8-sig")
        # data = json.loads(f.read())
        # json_str = json.dumps(data, ensure_ascii=False)
        return jsonify(json_str)


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
