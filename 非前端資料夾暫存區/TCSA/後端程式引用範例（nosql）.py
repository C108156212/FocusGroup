from pymongo import MongoClient
from TCSA import TCSA

# TCSA 是分析情緒分數的核心，可以呼叫兩個函數：
#   Degree: 傳入一段文字語料，回傳情緒評極。評極範圍 0.00 ~ 10.0
#   Orientation: 傳入一段文字語料，回傳情緒判斷結果。「Positive」「Negative」

# Step1: 準備一個名為 Data 的資料庫（database）（Data這個命名可改）

# Step2: 準備一個名為 Dcard 的資料表（collection）（Dcard這個命名可改）

# Step3: 建立 nosql 連線
client = MongoClient(host='localhost', port=27017)
db = client['Data']
collection = db.Dcard
# 只篩選留言的欄位 暫定欄位名稱為 "comment"
table = collection.find({},{'comment': True})
# collection.find({},{"word":True}) 查詢結果篩選 word 欄位
# collection.find({},{"value":False}) 查詢結果排除 value 欄位
# collection.find({"name":"Jone"})  查詢結果篩選 [name=Jone] 的資料
# collection.find({},{"value":{$gt:60}})  #查詢 value 大於60的資料
# collection.findOne() 查詢下一筆資料
# collection.find().sort({"column":1}) column 欄位遞增排序(1)、遞減排序(0)
# collection.find().count() 回傳資料筆數
# collection.find().limit(100) 回傳前100筆查詢結果

# Step4: 迴圈讀取範例
while True:
    print('--------------------')
    n = int(input("讀取陣列："))
    data = table[n]['comment']
    print('{}{}'.format("留言內容：", data))
    print('{}{}'.format("情緒評極：", TCSA.Degree(data)))
    print('{}{}'.format("情緒取向：", TCSA.Orientation(data)))
