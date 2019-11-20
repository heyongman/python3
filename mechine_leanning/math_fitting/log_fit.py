import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def fun(x, y):
    w = np.sqrt(y)
    polynomial = np.polyfit(x, np.log(np.log(y)), 1, w=w)
    return polynomial
    # print(polynomial)
    # p = np.poly1d(polynomial)
    # print(p)
    # print('%.3f = %.3f' % (np.log(20), 0.06009 * 30 + 1.416))
    # np.log(7) = 0.06009 * 19 + 1.416


if __name__ == '__main__':
    data = pd.read_csv('C:\\proj-20190610\\proj\\py_proj\\python3\\mechine_leanning\\math_fitting\\data.csv')
    # data = data['0'] + 1
    y = data['data'].values
    # x = np.array([10, 19, 30, 35, 51])
    # y = np.array([1, 7, 20, 50, 79])
    x = np.arange(1, len(data)+1)
    # y = data

    polynomial = fun(x, y)
    print(polynomial)
    a = polynomial[0]
    b = polynomial[1]

    # x1 = np.arange(0, 110)
    y1 = np.exp(np.exp(polynomial[0] * x + polynomial[1]))

    plt.plot(x, y, '.', label='sample')  # 样本数据
    plt.plot(x, y1, '-', label='fitting')  # 拟合数据

    plt.title("Fitting demo")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()
    plt.show()
