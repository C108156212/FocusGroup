# TCSA（Traditional Chinese Sentiment Analysis）繁體中文情緒分析

TCSA 是分析情緒分數的核心，可以呼叫兩個函數：  
Degree: 傳入一段文字語料，回傳情緒評極。評極範圍 0.00 ~ 10.0  
Orientation: 傳入一段文字語料，回傳情緒判斷結果。「Positive」「Negative」  


## [訓練模型下載](https://mega.nz/fm/moZW2a7K)
訓練模型來源：[酒店外賣評論資料](https://github.com/SophonPlus/ChineseNlpCorpus)

## 套件需求
* jieba 中文斷詞套件
```
pip install jieba
```
* torch 自然語言處理套件
```
pip install torch
```
* pandas 資料格式套件
```
pip install pandas
```
* mongo NoSQL資料庫套件
```
pip install mongo
```
