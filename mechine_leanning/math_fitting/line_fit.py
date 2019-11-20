import math
import numpy as np
from matplotlib import pyplot as plt


def line_fit(x, y):
    N = float(len(x))
    sx, sy, sxx, syy, sxy = 0, 0, 0, 0, 0
    for i in range(0, int(N)):
        sx += x[i]
        sy += y[i]
        sxx += x[i] * x[i]
        syy += y[i] * y[i]
        sxy += x[i] * y[i]
    a = (sy * sx / N - sxy) / (sx * sx / N - sxx)
    b = (sy - a * sx) / N
    r = abs(sy * sx / N - sxy) / math.sqrt((sxx - sx * sx / N) * (syy - sy * sy / N))
    return a, b, r


if __name__ == '__main__':
    X = np.array([1, 2, 3, 4, 5, 6])
    Y = np.array([2.5, 3.51, 4.45, 5.52, 6.47, 7.51])
    a, b, r = line_fit(X, Y)

    # or:
    arr = np.polyfit(X, Y, 1)
    p = np.poly1d(arr)
    # print(arr)
    print("拟合结果:", p)

    print("拟合结果: y = %.5f x + %.5f , r=%.5f" % (a, b, r))
    Y1 = a*X + b

    plt.plot(X, Y, '.', label='sample')  # 样本数据
    plt.plot(X, Y1, '-', label='fitting')  # 拟合数据

    plt.title("Fitting demo")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()
    plt.show()

