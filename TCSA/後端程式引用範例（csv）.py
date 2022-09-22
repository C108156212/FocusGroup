import pathlib
import pandas
from TCSA import TCSA

# TCSA 是分析情緒分數的核心，可以呼叫兩個函數：
#   Degree: 傳入一段文字語料，回傳情緒評極。評極範圍 0.00 ~ 10.0
#   Orientation: 傳入一段文字語料，回傳情緒判斷結果。「Positive」「Negative」

# Step1: 準備留言資料（.csv）並放在根目錄下

# Step2: 從 csv 檔中讀取留言資料
comment = '\\comment.csv'
root = '{}{}'.format(pathlib.Path(__file__).parent, comment)
converters = {
    'comment': str
    }
data = pandas.read_csv(root, converters = converters, encoding = 'utf-8')

# Step3: 迴圈讀取範例
while True:
    print('--------------------')
    n = int(input("讀取陣列："))
    print('{}{}'.format("留言內容：", data['comment'][n]))
    print('{}{}'.format("情緒評極：", TCSA.Degree(data['comment'][n])))
    print('{}{}'.format("情緒取向：", TCSA.Orientation(data['comment'][n])))
