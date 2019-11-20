import os
import pandas as pd
import numpy as np
import xlrd
import re


# 统计的期数
num_periods = 20
# 显示所有列
pd.set_option('display.max_columns', None)
# 使用pandas从excel中读取数据
src = pd.read_excel('/Users/he/Documents/daletou.xlsx',
                    names=['no', 'f1', 'f2', 'f3', 'f4', 'f5', 'b1', 'b2'],
                    skiprows=[1, 2, 3, 4, 5, 6],
                    usecols=8)
# 获取所需的期数数据
src = src[:num_periods]
print(src[:1])


# 获取号码为i的本次遗漏
def get_curr_miss(i, num):
    index = 'b' if num == 3 else 'f'
    m_a = []
    for x in range(1, num):
        m_a += src.index[src['%s%s' % (index, x)] == i].tolist()
    m_a.sort()
    curr_miss = num_periods if not m_a else m_a[0]
    return curr_miss


def area_data(area_num):
    # area_num为36或13
    # 抽取次数+1（前后区）
    extract_nums = 6 if area_num == 36 else 3
    # 生成一个计算数据结果的DF（前区号码，实际出现次数，理论出现次数，出现频率，平均遗漏，本次遗漏。。。）
    front_num = np.arange(1, area_num)
    res = pd.DataFrame(front_num, columns=['num_front'], index=range(1, area_num))
    # 统计各号码的出现次数
    res['real_occ'] = 0
    for i in range(1, extract_nums):
        res['f%s' % i] = src['f%s' % i].value_counts()
        res.fillna(0, inplace=True)
        res['real_occ'] += res['f%s' % i]
        res.pop('f%s' % i)

    # 统计理论出现次数
    res['theory_occ'] = num_periods / ((area_num-1)/(extract_nums-1))  # (area_num-1)/(extract_nums-1)

    # 统计出现频率
    res['p_occ'] = res['real_occ'] / num_periods

    # 统计平局遗漏
    res['aver_miss'] = (num_periods - res['real_occ']) / (res['real_occ']+1)

    # 统计本次遗漏
    curr_miss_list = []
    for i in range(1, area_num):
        curr_miss_list.append(get_curr_miss(i, extract_nums))  # 6,3
    res['curr_miss'] = curr_miss_list

    # 统计预出率
    res['pre_out_rate'] = res['curr_miss'] / res['aver_miss']

    # 根据预出率排序
    sort_col = 'pre_out_rate' if area_num == 13 else 'aver_miss'
    res.sort_values(by='pre_out_rate', axis=0, ascending=True, inplace=True)
    # res.pop('num_front')

    return res


front_data = area_data(36)
back_data = area_data(13)

print(front_data)
print(back_data)

last = list(src.iloc[0])[1:6]
f_f = front_data['num_front'].tolist()
f = [x for x in f_f if x not in last]
print(f)
print(back_data['num_front'].tolist())
