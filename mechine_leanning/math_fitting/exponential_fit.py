import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd


def func(x, a, b, c):
    return a * np.exp(-b * x) + c


if __name__ == '__main__':
    data = pd.read_csv('C:\\proj-20190610\\proj\\py_proj\\python3\\mechine_leanning\\math_fitting\\data.csv')
    # data = data['0'] + 1
    y = data['data'].values
    # x = np.array([10, 19, 30, 35, 51])
    # y = np.array([1, 7, 20, 50, 79])
    # x = np.arange(0, len(data))
    x = np.linspace(0, 10, len(data))
    popt, pcov = curve_fit(func, x, y)
    print(popt[0], popt[1], popt[2])
    y1 = [func(i, popt[0], popt[1], popt[2]) for i in x]

    plt.plot(x, y, '.', label='sample')  # 样本数据
    plt.plot(x, y1, '-', label='fitting')  # 拟合数据

    plt.title("Fitting demo")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()
    plt.show()
