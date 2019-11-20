import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import seaborn as sns
from pyspark.sql import SparkSession
from matplotlib.font_manager import _rebuild


# 箱型图
def boxplot():
    df = pd.read_csv('/Users/he/work/bigdata/docu/db/catering_sale.csv', header=0)
    # print(bp.count())
    # print(bp.describe())
    plt.figure()
    # 当指定return_type=‘dict’时，其结果值为一个字典，
    # 字典索引为固定的'whiskers'、'caps'、'boxes'、'fliers'、'means'
    bp = df.boxplot(return_type='dict')
    # flies为异常值的标签
    x = bp['fliers'][0].get_xdata()
    y = bp['fliers'][0].get_ydata()
    y.sort()
    print(y)
    # 用annotate添加注释
    for i in range(len(x)):
        plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i] + 0.1 - 0.8 / (y[i] - y[i - 1]), y[i]))
    plt.show()


# 折线图
def lineplot():
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    ts.plot()

    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
    df = df.cumsum()
    df.plot()
    plt.legend(loc='best')

    # 对数据框相同索引分列分别作图
    df.plot(subplots=True, figsize=(6, 6))
    plt.legend(loc='best')
    plt.show()


# 条形图
def barplot():
    spark = SparkSession.builder.appName('data_explore').master('local[4]').getOrCreate()
    hourDF = spark.read.csv('/Users/he/work/bigdata/docu/db/ml-100k/u.user', sep="|").toDF('name','age','gender','occupation','zip')
    hourDF.show(truncate=False)
    hourDF.createTempView('user')
    count_occp = spark.sql("SELECT occupation,count(occupation) as cnt FROM user Group by occupation order by cnt")
    # count_occp.show(truncate=False)
    # 获取职业名称及职业数，以便画出各职业对应总数图形
    # 把运行结果转换为RDD
    x_axis = count_occp.rdd.map(lambda p: p.occupation).collect()
    y_axis = count_occp.rdd.map(lambda p: p.cnt).collect()

    pos = np.arange(len(x_axis))
    width = 1.0
    # 隐式新增一个figure，或为当前figure新增一个axes
    ax = plt.axes()
    ax.set_xticks(pos + (width / 2))  # 设置x轴刻度
    ax.set_xticklabels(x_axis)  # 在对应刻度打上标签
    plt.bar(pos, y_axis, width, color='orange')
    plt.xticks(rotation=30)  # x轴上的标签旋转30度
    fig = plt.gcf()  # 获取当前figure的应用
    fig.set_size_inches(16, 10)  # 设置当前figure大小
    plt.show()


# 特征分布及相关性分析
def pairplot():
    pd.set_option('display.max_columns', None)
    data_pd = pd.read_csv('/Users/he/work/bigdata/docu/db/hour.csv', header=0)
    # data_pd = data1.toPandas()
    sns.set(style='whitegrid', context='notebook')
    cols = ['season','yr','temp','atemp','hum','windspeed','cnt']
    sns.pairplot(data_pd[cols], height=2.5)
    plt.show()


# 对比分析
def compareplot():
    # 把日期列作为索引，并转换为日期格式
    df = pd.read_csv("/Users/he/work/bigdata/docu/db/catering_sale.csv", header=0, index_col='日期', parse_dates=True)
    # 把空值置为0
    df1 = df.fillna(0)
    # 根据年月求和
    df_ym = df1.resample('M').sum()
    # 取年月
    df2 = df_ym.to_period('M')
    print(df2)
    # # 数据可视化
    df2.plot(kind='bar', rot=30)
    plt.legend()
    plt.show()


def sinplot():
    x = np.linspace(0, 10, 100)  # linspace (起点，终点，元素个数)
    y = np.sin(x)
    y1 = np.cos(x)
    # 绘制一个图，长为10，宽为6（默认值是每个单位80像素）
    plt.figure(figsize=(10, 6))
    # 在图列中自动显示$间内容,$感觉也没什么用
    plt.plot(x, y, label="$sin(x)$", color="red", linewidth=2)
    plt.plot(x, y1, "b--", label="$cos(x^2)$")  # b（blue），--线形
    plt.xlabel("X值")  # X坐标名称，u表示unicode编码
    plt.ylabel("Y值")
    plt.title("三角函数图像")  # t图名称
    plt.ylim(-1.2, 1.2)  # y上的max、min值
    plt.legend()  # 显示图例
    plt.grid()  # 显示网格
    plt.savefig('fig01.svg', format='svg')  # 保持到当前目录
    plt.show()


def test():
    _rebuild()


if __name__ == '__main__':
    # boxplot()  # 箱型图
    # lineplot()  # 折线图
    # barplot()  # 条形图
    # pairplot()  # 特征分布及相关性分析
    # compareplot()  # 对比分析
    sinplot()  # 三角函数
    # test()
