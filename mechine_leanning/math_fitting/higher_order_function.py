import numpy
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def second_order_function():
    x = [1, 2, 3, 4, 5, 6]
    y = [2.5, 3.51, 4.45, 5.52, 6.47, 7.2]
    degree = 2

    results = {}
    coeffs = numpy.polyfit(x, y, degree)
    results['polynomial'] = coeffs

    # r-squared
    p = numpy.poly1d(coeffs)
    print(p)
    # fit values, and mean
    yhat = p(x)  # or [p(z) for z in x]
    ybar = numpy.sum(y) / len(y)  # or sum(y)/len(y)
    ssreg = numpy.sum((yhat - ybar) ** 2)  # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = numpy.sum((y - ybar) ** 2)  # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot  # 准确率
    print(results)


def higher_order_function():
    data = pd.read_csv('C:\\proj-20190610\\proj\\py_proj\\python3\\mechine_leanning\\math_fitting\\data.csv')
    y = data['data'].values
    x = np.arange(1, len(y) + 1)

    degree = 2
    coefficients = np.polyfit(x, y, degree)
    print(coefficients)
    p = np.poly1d(coefficients)
    print(p)
    # return
    y1 = []
    for xi in x:
        yi = 0.0
        for i in range(degree, -1, -1):
            print(coefficients[degree - i])
            yi += (coefficients[degree - i] * pow(xi, i))
        y1.append(yi)
    y1 = np.array(y1)
    # print(y1)
    # return
    plt.plot(x, y, '.', label='sample')  # 样本数据
    plt.plot(x, y1, '-', label='fitting')  # 拟合数据

    plt.title("Fitting demo")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()
    plt.show()


if __name__ == '__main__':
    # second_order_function()
    higher_order_function()
