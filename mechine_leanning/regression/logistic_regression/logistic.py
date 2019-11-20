# coding:utf-8

from scipy import fft
from scipy.io import wavfile
from scipy.stats import norm
from sklearn import linear_model, datasets
from sklearn.linear_model import LogisticRegression

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
使用logistic regression处理音乐数据,音乐数据训练样本的获得和使用快速傅里叶变换（FFT）预处理的方法需要事先准备好
1. 把训练集扩大到每类100个首歌,类别仍然是六类:jazz,classical,country, pop, rock, metal
2. 同时使用logistic回归训练模型
3. 引入一些评价的标准来比较Logistic测试集上的表现 
"""


# 准备音乐数据
def create_fft(g, n):
    #      /Users/he/work/bigdata/media/机器学习与数据挖掘/02-回归算法/资料/genres/classical/converted/classical.00000.au.wav
    rad = "/Users/he/work/bigdata/media/机器学习与数据挖掘/02-回归算法/资料/genres/%s/converted/%s.%s.au.wav" % (g, g, str(n).zfill(5))
    # sample_rate 音频的采样率，X代表读取文件的所有信息
    (sample_rate, X) = wavfile.read(rad)
    print(sample_rate)
    # 取1000个频率特征  也就是振幅
    fft_features = abs(fft(X)[:1000])
    # zfill(5) 字符串不足5位，前面补0
    sad = "/Users/he/work/bigdata/media/机器学习与数据挖掘/02-回归算法/资料/genres/%s/%s.%s.fft" % (g, g, str(n).zfill(5))
    # np.savetxt(sad, fft_features, fmt='%10.5f')
    # np.save('aaaa', fft_features)
    return fft_features


def create_train_data():
    # -------create fft 构建训练集--------------
    genre_list = ["classical", "jazz", "country", "pop", "rock", "metal", "hiphop"]
    for g in genre_list:
        df = pd.DataFrame(columns=range(1000))
        for n in range(100):
            fft_features = create_fft(g, n)
            df.loc[g+str(n)] = fft_features
            print('running...')
        # 保存一个类型的特征
        print(df)
        sad = "/Users/he/work/bigdata/media/机器学习与数据挖掘/02-回归算法/资料/genres/%s/%s.fft" % (g, g)
        with open(sad, 'w+') as f:
            f.write(df.to_string(header=False, float_format='%10.5f', justify='unset'))
    print('finished')


def predict():
    # =========================================================================================
    # 加载训练集数据,分割训练集以及测试集,进行分类器的训练
    # 构造训练集！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # -------read fft--------------
    genre_list = ["classical", "jazz", "country", "pop", "rock", "metal", "hiphop"]
    X = []
    Y = []
    for g in genre_list:
        for n in range(100):
            rad = "/Users/he/work/bigdata/media/机器学习与数据挖掘/02-回归算法/资料/genres/%s/%s.fft" % (g, g)
            # 加载文件
            # fft_features = np.load(rad)
            fft_features = np.loadtxt(rad)
            X.append(fft_features)
            # genre_list.index(g) 返回匹配上类别的索引号
            Y.append(genre_list.index(g))

    # 构建的训练集
    X = np.array(X)
    # 构建的训练集对应的类别
    Y = np.array(Y)

    # 接下来，我们使用sklearn，来构造和训练我们的两种分类器
    # ------train logistic classifier--------------
    model = LogisticRegression()
    # 需要numpy.array类型参数
    model.fit(X, Y)

    print('Starting read wavfile...')
    # prepare test data-------------------
    # sample_rate, test = wavfile.read("i:/classical.00007.au.wav")
    sample_rate, test = wavfile.read("/Users/he/work/bigdata/media/机器学习与数据挖掘/02-回归算法/资料/genres/heibao-wudizirong-remix.wav")
    print(sample_rate, test)
    testdata_fft_features = abs(fft(test))[:1000]
    # model.predict(testdata_fft_features) 预测为一个数组，array([类别])
    type_index = model.predict(testdata_fft_features)[0]
    print(type_index)
    print(genre_list[type_index])


if __name__ == '__main__':
    # create_fft('classical', 0)
    # create_train_data()
    predict()
