from pymongo import MongoClient
import calendar
from datetime import datetime

# 關鍵字搜尋
def KeySearch(keyword="#", period="day"):
    # 宣告回傳值變數
    CommentCount = 0
    LastCommentCount = 0
    CommentAmount = "{:.0%}".format(0)
    CommentLabel = "none"
    PositiveCount = 0
    LastPositiveCount = 0
    PositiveAmount = "{:.0%}".format(0)
    PositiveLabel = "none"
    NegativeCount = 0
    LastNegativeCount = 0
    NegativeAmount = "{:.0%}".format(0)
    NegativeLabel = "none"
    NeutralCount = 0
    LastNeutralCount = 0
    NeutralAmount = "{:.0%}".format(0)
    NeutralLabel = "none"
    ChartDescription = "none"
    ChartDate = "none"
    match period:
        case "month":
            Datanum = [0] * datetime.today().month
            ChartData = {
                "labels": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
                "datasets": {"label": "本月熱度取向", "data": Datanum}
            }
        case "week":
            Datanum = [0] * datetime.weekday(datetime.today())
            ChartData = {
                "labels": ["週日", "週一", "週二", "週三", "週四", "週五", "週六"],
                "datasets": {"label": "本日熱度取向", "data": Datanum}
            }
        case "day":
            dayrange = calendar.monthrange(datetime.today().year,datetime.today().month)[1]
            Datanum = [0] * datetime.today().day
            labels = list(range(1, dayrange + 1, 1))
            ChartData = {
                "labels": labels,
                "datasets": {"label": "本日熱度取向", "data": Datanum}
            }
        case "hour":
            hourrange = datetime.now().hour
            Datanum = [0] * hourrange
            labels = list(range(24))
            ChartData = {
                "labels": labels,
                "datasets": {"label": "本日熱度取向", "data": Datanum}
            }

    # 連線 Mongo 資料庫
    client = MongoClient(
        host="mongodb+srv://1100137146:7553@cluster0.fo8ynch.mongodb.net/test")
        # host="mongodb+srv://Crawler_admin:Crawling15622@cluster0.sc0f7sr.mongodb.net/test")
    db = client["FocusGroup"]
    article = db["article"]
    comment = db["comment"]

    # 由資料庫「article」中篩選「title, in:關鍵字」的資料 並將其「id」組成陣列
    article_Id = []
    filter = {"title": {"$regex": keyword}}
    article_table = article.find(filter)
    for article_n in range(article_table.collection.count_documents(filter)):
        article_Id.append(article_table[article_n]["id"])
    
    # 依期間（月、週、日、時）選擇執行
    match period:
        case "month":
            # 本月留言數：由資料庫「comment」中篩選「postId:文章ID, {month:updatedAt}:本月」的資料
            filter = {"postId": {"$in": article_Id}, "$expr": {"$eq": [{"$month": "$updatedAt"}, datetime.today().month]}}
            comment_table = comment.find(filter)
            CommentCount = comment_table.collection.count_documents(filter)
            # 上月留言數：由資料庫「comment」中篩選「postId:文章ID, {month:updatedAt}:上月」的資料
            filter = {"postId": {"$in": article_Id}, "$expr": {"$eq": [{"$month": "$updatedAt"}, datetime.today().month - 1]}}
            comment_table = comment.find(filter)
            LastCommentCount = comment_table.collection.count_documents(filter)
            # 本月正面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Positive", {month:updatedAt}:本月」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Positive", "$expr": {"$eq": [{"$month": "$updatedAt"}, datetime.today().month]}}
            comment_table = comment.find(filter)
            PositiveCount = comment_table.collection.count_documents(filter)
            # 上月正面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Positive", {month:updatedAt}:上月」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Positive", "$expr": {"$eq": [{"$month": "$updatedAt"}, datetime.today().month - 1]}}
            comment_table = comment.find(filter)
            LastPositiveCount = comment_table.collection.count_documents(filter)
            # 本月負面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Negative", {month:updatedAt}:本月」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Negative", "$expr": {"$eq": [{"$month": "$updatedAt"}, datetime.today().month]}}
            comment_table = comment.find(filter)
            NegativeCount = comment_table.collection.count_documents(filter)
            # 上月負面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Negative", {month:updatedAt}:上月」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Negative", "$expr": {"$eq": [{"$month": "$updatedAt"}, datetime.today().month - 1]}}
            comment_table = comment.find(filter)
            LastNegativeCount = comment_table.collection.count_documents(filter)
            # 本月中立留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Neutral", {month:updatedAt}:本月」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Neutral", "$expr": {"$eq": [{"$month": "$updatedAt"}, datetime.today().month]}}
            comment_table = comment.find(filter)
            NeutralCount = comment_table.collection.count_documents(filter)
            # 上月中立留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Neutral", {month:updatedAt}:上月」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Neutral", "$expr": {"$eq": [{"$month": "$updatedAt"}, datetime.today().month - 1]}}
            comment_table = comment.find(filter)
            LastNeutralCount = comment_table.collection.count_documents(filter)

            for i in range(datetime.today().month):
                # 時間戳記
                t_month = i + 1
                # 依月份合計情緒分數：由資料庫「comment」中篩選「postId:文章ID」依「month:updatedAt」群組合計「degree」與「資料筆數」的資料
                filter = [{"$match": {"postId": {"$in": article_Id}, "$expr": {"$eq": [{"$month": "$updatedAt"}, t_month]}}}, {"$group": {"_id": { "$month": "$updatedAt"}, "total": {"$sum": "$degree"}, "num": {"$sum": 1}}}]
                comment_table = comment.aggregate(filter)
                if comment_table.alive:
                    comment_table = list(comment_table)
                    total = comment_table[0]["total"]
                    num = comment_table[0]["num"]
                    Datanum[i] = "%.3f" % (total / num)
        case "week":
            # 時間戳記
            t = datetime.today()
            t_this = datetime.toordinal(t) - datetime.weekday(datetime.today())
            t_this = datetime.fromordinal(t_this)
            t_this = datetime.strftime(t_this, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            t_this = datetime.strptime(t_this, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            t_last = datetime.toordinal(t) - datetime.weekday(datetime.today()) + 7
            t_last = datetime.fromordinal(t_last)
            t_last = datetime.strftime(t_last, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            t_last = datetime.strptime(t_last, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            # 本週留言數：由資料庫「comment」中篩選「postId:文章ID, updatedAt:<本週」的資料
            filter = {"postId": {"$in": article_Id}, "updatedAt": {"$gt": t_this}}
            comment_table = comment.find(filter)
            CommentCount = comment_table.collection.count_documents(filter)
            # 上週留言數：由資料庫「comment」中篩選「postId:文章ID, updatedAt:>=本週,<上週」的資料
            filter = {"postId": {"$in": article_Id}, "updatedAt": {"$lte": t_this, "$gt": t_last}}
            comment_table = comment.find(filter)
            LastCommentCount = comment_table.collection.count_documents(filter)
            # 本週正面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Positive", updatedAt:<本週」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Positive", "updatedAt": {"$gt": t_this}}
            comment_table = comment.find(filter)
            PositiveCount = comment_table.collection.count_documents(filter)
            # 上週正面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Positive", updatedAt:>=本週,<上週」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Positive", "updatedAt": {"$lte": t_this, "$gt": t_last}}
            comment_table = comment.find(filter)
            LastPositiveCount = comment_table.collection.count_documents(filter)
            # 本週負面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Negative", updatedAt:<本週」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Negative", "updatedAt": {"$gt": t_this}}
            comment_table = comment.find(filter)
            NegativeCount = comment_table.collection.count_documents(filter)
            # 上週負面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Negative", updatedAt:>=本週,<上週」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Negative", "updatedAt": {"$lte": t_this, "$gt": t_last}}
            comment_table = comment.find(filter)
            LastNegativeCount = comment_table.collection.count_documents(filter)
            # 本週中立留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Neutral", updatedAt:<本週」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Neutral", "updatedAt": {"$gt": t_this}}
            comment_table = comment.find(filter)
            NeutralCount = comment_table.collection.count_documents(filter)
            # 上週中立留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Neutral", updatedAt:>=本週,<上週」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Neutral", "updatedAt": {"$lte": t_this, "$gt": t_last}}
            comment_table = comment.find(filter)
            LastNeutralCount = comment_table.collection.count_documents(filter)

            for i in range(datetime.weekday(datetime.today())):
                # 時間戳記
                t_weekday = datetime.toordinal(t) - i
                t_weekday = datetime.fromordinal(t_weekday)
                t_weekday = datetime.strftime(t_weekday, "%Y-%m-%d")
                # 依星期合計情緒分數：由資料庫「comment」中篩選「postId:文章ID」依「日期」群組合計「degree」與「資料筆數」的資料再篩選「本週星期」的資料
                filter = [{"$match": {"postId": {"$in": article_Id}}}, {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, "total": {"$sum": "$degree"}, "num": {"$sum": 1}}}, {"$match": {"_id": t_weekday}}]
                comment_table = comment.aggregate(filter)
                if comment_table.alive:
                    comment_table = list(comment_table)
                    total = comment_table[0]["total"]
                    num = comment_table[0]["num"]
                    Datanum[i] = "%.3f" % (total / num)
        case "day":
            # 時間戳記
            t = datetime.today()
            t_this = datetime.toordinal(t) - 1
            t_this = datetime.fromordinal(t_this)
            t_this = datetime.strftime(t_this, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            t_this = datetime.strptime(t_this, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            t_last = datetime.toordinal(t) - 2
            t_last = datetime.fromordinal(t_last)
            t_last = datetime.strftime(t_last, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            t_last = datetime.strptime(t_last, "%Y-%m-%dT%H:%M:%S.%f+00:00")
            # 本日留言數：由資料庫「comment」中篩選「postId:文章ID, updatedAt:<本日」的資料
            filter = {"postId": {"$in": article_Id}, "updatedAt": {"$eq": t_this}}
            comment_table = comment.find(filter)
            CommentCount = comment_table.collection.count_documents(filter)
            # 上日留言數：由資料庫「comment」中篩選「postId:文章ID, updatedAt:>=本日,<上日」的資料
            filter = {"postId": {"$in": article_Id}, "updatedAt": {"$lte": t_this, "$gt": t_last}}
            comment_table = comment.find(filter)
            LastCommentCount = comment_table.collection.count_documents(filter)
            # 本日正面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Positive", updatedAt:<本日」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Positive", "updatedAt": {"$gt": t_this}}
            comment_table = comment.find(filter)
            PositiveCount = comment_table.collection.count_documents(filter)
            # 上日正面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Positive", updatedAt:>=本日,<上日」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Positive", "updatedAt": {"$lte": t_this, "$gt": t_last}}
            comment_table = comment.find(filter)
            LastPositiveCount = comment_table.collection.count_documents(filter)
            # 本日負面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Negative", updatedAt:<本日」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Negative", "updatedAt": {"$gt": t_this}}
            comment_table = comment.find(filter)
            NegativeCount = comment_table.collection.count_documents(filter)
            # 上日負面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Negative", updatedAt:>=本日,<上日」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Negative", "updatedAt": {"$lte": t_this, "$gt": t_last}}
            comment_table = comment.find(filter)
            LastNegativeCount = comment_table.collection.count_documents(filter)
            # 本日中立留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Neutral", updatedAt:<本日」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Neutral", "updatedAt": {"$gt": t_this}}
            comment_table = comment.find(filter)
            NeutralCount = comment_table.collection.count_documents(filter)
            # 上日中立留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Neutral", updatedAt:>=本日,<上日」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Neutral", "updatedAt": {"$lte": t_this, "$gt": t_last}}
            comment_table = comment.find(filter)
            LastNeutralCount = comment_table.collection.count_documents(filter)

            for i in range(datetime.today().day):
                # 時間戳記
                t_day = datetime.toordinal(t) - i
                t_day = datetime.fromordinal(t_day)
                t_day = datetime.strftime(t_day, "%Y-%m-%d")
                # 依日期合計情緒分數：由資料庫「comment」中篩選「postId:文章ID」依「日期」群組合計「degree」與「資料筆數」的資料再篩選「日期」的資料
                filter = [{"$match": {"postId": {"$in": article_Id}}}, {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, "total": {"$sum": "$degree"}, "num": {"$sum": 1}}}, {"$match": {"_id": t_day}}]
                comment_table = comment.aggregate(filter)
                if comment_table.alive:
                    comment_table = list(comment_table)
                    total = comment_table[0]["total"]
                    num = comment_table[0]["num"]
                    Datanum[i] = "%.3f" % (total / num)
        case "hour":
            # 時間戳記
            t_today = datetime.strftime(datetime.today(), "%Y-%m-%d")
            # 本時留言數：由資料庫「comment」中篩選「postId:文章ID, updatedAt:本日,本時」的資料
            filter = {"postId": {"$in": article_Id}, "$expr": {"$eq": [{"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, t_today], "$eq": [{"$hour": "$updatedAt"}, datetime.now().hour]}}
            comment_table = comment.find(filter)
            CommentCount = comment_table.collection.count_documents(filter)
            # 上時留言數：由資料庫「comment」中篩選「postId:文章ID, updatedAt:本日,上時」的資料
            filter = {"postId": {"$in": article_Id}, "$expr": {"$eq": [{"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, t_today], "$eq": [{"$hour": "$updatedAt"}, datetime.now().hour - 1]}}
            comment_table = comment.find(filter)
            LastCommentCount = comment_table.collection.count_documents(filter)
            # 本時正面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Positive", updatedAt:本日,本時」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Positive", "$expr": {"$eq": [{"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, t_today], "$eq": [{"$hour": "$updatedAt"}, datetime.now().hour]}}
            comment_table = comment.find(filter)
            PositiveCount = comment_table.collection.count_documents(filter)
            # 上時正面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Positive", updatedAt:本日,上時」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Positive", "$expr": {"$eq": [{"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, t_today], "$eq": [{"$hour": "$updatedAt"}, datetime.now().hour - 1]}}
            comment_table = comment.find(filter)
            LastPositiveCount = comment_table.collection.count_documents(filter)
            # 本時負面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Negative", updatedAt:本日,本時」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Negative", "$expr": {"$eq": [{"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, t_today], "$eq": [{"$hour": "$updatedAt"}, datetime.now().hour]}}
            comment_table = comment.find(filter)
            NegativeCount = comment_table.collection.count_documents(filter)
            # 上時負面留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Negative", updatedAt:本日,上時」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Negative", "$expr": {"$eq": [{"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, t_today], "$eq": [{"$hour": "$updatedAt"}, datetime.now().hour - 1]}}
            comment_table = comment.find(filter)
            LastNegativeCount = comment_table.collection.count_documents(filter)
            # 本時中立留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Neutral", updatedAt:本日,本時」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Neutral", "$expr": {"$eq": [{"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, t_today], "$eq": [{"$hour": "$updatedAt"}, datetime.now().hour]}}
            comment_table = comment.find(filter)
            NeutralCount = comment_table.collection.count_documents(filter)
            # 上時中立留言數：由資料庫「comment」中篩選「postId:文章ID, orientation:"Neutral", updatedAt:本日,上時」的資料
            filter = {"postId": {"$in": article_Id}, "orientation": "Neutral", "$expr": {"$eq": [{"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, t_today], "$eq": [{"$hour": "$updatedAt"}, datetime.now().hour - 1]}}
            comment_table = comment.find(filter)
            LastNeutralCount = comment_table.collection.count_documents(filter)

            for i in range(datetime.now().hour):
                # 時間戳記
                t_hour = i
                # 依日期合計情緒分數：由資料庫「comment」中篩選「postId:文章ID, updatedAt:本日」依「時刻」群組合計「degree」與「資料筆數」的資料再篩選「時刻」的資料
                filter = [{"$match": {"postId": {"$in": article_Id}, "$expr": {"$eq": [{"$dateToString": {"format": "%Y-%m-%d", "date": "$updatedAt"}}, t_today]}}}, {"$group": {"_id": {"$hour": "$updatedAt"}, "total": {"$sum": "$degree"}, "num": {"$sum": 1}}}, {"$match": {"_id": t_hour}}]
                comment_table = comment.aggregate(filter)
                if comment_table.alive:
                    comment_table = list(comment_table)
                    total = comment_table[0]["total"]
                    num = comment_table[0]["num"]
                    Datanum[i] = "%.3f" % (total / num)

    # 留言數成長比率
    if LastCommentCount > 0:
        CommentAmount = "{:.0%}".format(CommentCount / LastCommentCount * 100)
        CommentLabel = "較上期增加" if CommentCount / LastCommentCount < 0 else "較上期減少"
    else:
        CommentLabel = "無本期資料" if CommentCount == 0 else "無上期資料"
    # 正面留言數成長比率
    if LastPositiveCount > 0:
        PositiveAmount = "{:.0%}".format(PositiveCount / LastPositiveCount * 100)
        PositiveLabel = "較上期增加" if PositiveCount / LastPositiveCount < 0 else "較上期減少"
    else:
        PositiveLabel = "無本期資料" if PositiveCount == 0 else "無上期資料"
    # 負面留言數成長比率
    if LastNegativeCount > 0:
        NegativeAmount = "{:.0%}".format(NegativeCount / LastNegativeCount * 100)
        NegativeLabel = "較上期增加" if NegativeCount / LastNegativeCount < 0 else "較上期減少"
    else:
        NegativeLabel = "無本期資料" if NegativeCount == 0 else "無上期資料"
    # 中立留言數成長比率
    if LastNeutralCount > 0:
        NeutralAmount = "{:.0%}".format(NeutralCount / LastNeutralCount * 100)
        NeutralLabel = "較上期增加" if NeutralCount / LastNeutralCount < 0 else "較上期減少"
    else:
        NeutralLabel = "無本期資料" if NeutralCount == 0 else "無上期資料"

    # JSON 標準化輸出 -> https://127.0.0.1:5000/dashboard
    return {
        "CommentCount": CommentCount,
        "CommentAmount": CommentAmount,
        "CommentLabel": CommentLabel,
        "PositiveCount": PositiveCount,
        "PositiveAmount": PositiveAmount,
        "PositiveLabel": PositiveLabel,
        "NegativeCount": NegativeCount,
        "NegativeAmount": NegativeAmount,
        "NegativeLabel": NegativeLabel,
        "NeutralCount": NeutralCount,
        "NeutralAmount": NeutralAmount,
        "NeutralLabel": NeutralLabel,
        "ChartDescription": ChartDescription,
        "ChartDate": ChartDate,
        "ChartData": ChartData
    }
