# 該函數用於評價句子正反面情緒與計算強烈程度

# TCSA（Traditional Chinese Sentiment Analysis）
# 繁體中文情緒分析
# 神經語言規劃 NLP（Neuro-Linguistic Programming）

import torch
from JWP import JWP
from gensim.models.doc2vec import Doc2Vec
import torch.nn.functional as F
import torch
import numpy as np
from W2V_SV import W2VS

class TCSA():
    def Degree(Sentiment):
        v1 = w2vs.getSenVec(Sentiment)
        res = net(torch.FloatTensor(v1), apply_sigmoid = True)
        out = res
        res = res.clone().detach().numpy()[0]
        return(round(res,3))

    def Orientation(Sentiment):
        v1 = w2vs.getSenVec(Sentiment)
        res = net(torch.FloatTensor(v1), apply_sigmoid = True)
        out = res
        res = res.clone().detach().numpy()[0]
        if(res>0.5):
            return("Positive")
        else:
            return("Negative")

w2vs = W2VS()
net = torch.load('torchmodel/pytorch_bce.model')
net.eval()
