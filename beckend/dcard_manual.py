# 每 60 秒，自動更新，由 Dcard API 提供的「美食版」資訊。

from time import sleep
from pymongo import MongoClient
import pathlib
import pandas

# 連線 Mongo 資料庫
client = MongoClient(host="mongodb+srv://1100137146:7553@cluster0.fo8ynch.mongodb.net/test")
db = client["FocusGroup"]
article = db["article"]
comment = db["comment"]
while True:
    # 由檔案取得「看版資訊」 因 Dcard 驗證碼機制 暫以手動下載的資料代替
    # request_url = "https://www.dcard.tw/service/api/v2/posts"
    request_root = "\\Dcard_API_PostData\\food.json"
    request_path = "{}{}".format(pathlib.Path(__file__).parent, request_root)
    request_file = pandas.read_json(request_path, encoding="utf-8")
    # 順序讀取「看版資訊」資料
    for request_n in request_file.index:
        article_table = article.find()
        id = str(request_file["id"][request_n])
        filter = {"id": id}
        # 判斷「文章」是否存在 存在則新增或更新 不存在則刪除此項紀錄
        try:
            title = str(request_file["title"][request_n])
            data = {"id": id, "title": title}
            # 判斷「文章」是否已建立於資料庫中 存在則更新 不存在則新增
            if article_table.collection.count_documents(filter) == 0:
                # 新增資料
                article.insert_one(data)
            else:
                # 更新資料 文章可能改名或更新
                newvalues = {"$set": data}
                article.update_one(filter, newvalues)
            # 由檔案取得「看版留言」 因 Dcard 驗證碼機制 暫以手動下載的資料代替
            # comment_url = "https://www.dcard.tw/service/api/v2/posts/" + str(request_file["id"][request_n]) + "/comments"
            comment_root = "\\Dcard_API_PostData\\" + str(request_file["id"][request_n]) + ".json"
            comment_path = "{}{}".format(pathlib.Path(__file__).parent, comment_root)
            comment_file = pandas.read_json(comment_path, encoding="utf-8")
            # 順序讀取「看版留言」資料
            for comment_n in comment_file.index:
                comment_table = comment.find()
                id = str(comment_file["id"][comment_n])
                filter = {"id": id}
                # 判斷「留言」是否存在 存在則新增或更新 不存在則刪除此項紀錄
                try:
                    postId = str(comment_file["postId"][comment_n])
                    updatedAt = str(comment_file["updatedAt"][comment_n])
                    content = str(comment_file["content"][comment_n])
                    data = {"id": id, "postId": postId,
                            "updatedAt": updatedAt, "content": content}
                    # 判斷「留言」是否已建立於資料庫中 存在則更新 不存在則新增
                    if comment_table.collection.count_documents(filter) == 0:
                        # 新增資料
                        comment.insert_one(data)
                    else:
                        # 更新資料 留言可能有更新
                        newvalues = {"$set": data}
                        comment.update_one(filter, newvalues)
                except:
                    # 刪除資料
                    comment.delete_one(filter)
        except:
            # 刪除資料
            article.delete_one(filter)
    # 每 30 秒重複執行
    sleep(60)

# Dcard_api_url = "https://www.dcard.tw/service/api/v2"
# 全部文章 GET /posts
# 看板資訊 GET /forums
# 看板內文章列表 GET /forums/{看板名稱}/posts
# 文章內文 GET /posts/{文章ID}
# 文章內引用連結 GET /posts/{文章ID}/links
# 文章內留言 GET /posts/{文章ID}/comments