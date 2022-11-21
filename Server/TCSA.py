# TCSA（Traditional Chinese Sentiment Analysis）繁體中文情緒分析
# 該函數用於評價句子正反面情緒與計算強烈程度

# TCSA 是分析情緒分數的核心，可以呼叫兩個函數：
#   Degree: 傳入一段文字語料，回傳情緒評極。評極範圍 0.00 ~ 10.0
#   Orientation: 傳入一段文字語料，回傳情緒判斷結果。「Positive」「Negative」

import torch
from JWP import JWP
from gensim.models.doc2vec import Doc2Vec
import torch.nn.functional as F
import torch
import numpy as np
from W2V_SV import W2VS
import pathlib

class TCSA():
    def Degree(Sentiment):
        v1 = w2vs.getSenVec(Sentiment)
        res = net(torch.FloatTensor(v1), apply_sigmoid = True)
        res = res.clone().detach().numpy()[0]
        return(round(res,3))

    def Orientation(Sentiment):
        v1 = w2vs.getSenVec(Sentiment)
        res = net(torch.FloatTensor(v1), apply_sigmoid = True)
        res = res.clone().detach().numpy()[0]
        match res: 
            case _ if res > 0.6:
                return("Positive")
            case _ if res < 0.4:
                return("Negative")
            case _ :
                return("Neutral")

w2vs = W2VS()
net = torch.load("{}{}".format(pathlib.Path(__file__).parent, "\\torchmodel\\pytorch_bce.model"))
net.eval()
