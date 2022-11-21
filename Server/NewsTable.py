from pymongo import MongoClient

# 最新留言版面
def NewsTable():
    # 宣告回傳值變數
    ArticleTitle = []
    ArticleURL = []
    ArticleOrientation = []
    CommentContent = []
    CommentOrientation = []

    # 連線 Mongo 資料庫
    client = MongoClient(
        host="mongodb+srv://1100137146:7553@cluster0.fo8ynch.mongodb.net/test")
    db = client["FocusGroup"]
    comment = db["comment"]

    # 由資料庫「comment」中篩選「最新10筆」的資料
    filter = [{"$sort": {"updatedAt": -1}}, {"$limit": 10}]
    data = list(comment.aggregate(filter))
    for i in range(10):
        # 「文章熱度」編號與連結
        ArticleTitle.append(data[i]['postId'])
        ArticleURL.append("https://www.dcard.tw/f/food/p/" + data[i]['postId'])
        # 「評論內容」
        CommentContent.append(data[i]['content'])
        # 「評論面向」
        match data[i]['orientation']:
            case "Positive":
                CommentOrientation.append("正面")
            case "Negative":
                CommentOrientation.append("負面")
            case "Neutral":
                CommentOrientation.append("中立")
        # 由資料庫「comment」中篩選「postId:文章ID」依「postId」群組合計「degree」與「資料筆數」的資料
        filter = [{"$match": {"postId": data[i]['postId']}}, {"$group": {"_id": "$postId", "total": {"$sum": "$degree"}, "num": {"$sum": 1}}}]
        data2 = list(comment.aggregate(filter))
        total = data2[0]["total"]
        num = data2[0]["num"]
        # 「文章熱度」面向
        ArticleOrientation.append("%.3f" % (total / num))

    # JSON 標準化輸出 -> https://127.0.0.1:5000/dashboard2
    return {
        "ArticleTitle": ArticleTitle,
        "ArticleURL": ArticleURL,
        "ArticleOrientation": ArticleOrientation,
        "CommentContent": CommentContent,
        "CommentOrientation": CommentOrientation
    }
