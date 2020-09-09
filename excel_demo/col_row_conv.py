import pandas as pd


def row2col_use_pivot():
    inputs = ['古明地觉', '语文', 91], \
             ['古明地觉', '数学', 95], \
             ['古明地觉', '英语', 96], \
             ['芙兰朵露', '语文', 87], \
             ['芙兰朵露', '数学', 92], \
             ['芙兰朵露', '英语', 98],
    data = pd.DataFrame(inputs).rename(columns={0: '姓名', 1: '科目', 2: '分数'})

    res = pd.pivot(data, index='姓名', columns='科目', values='分数') \
        .rename_axis(columns=None) \
        .reset_index()
    print(res)


def row2col_use_unstack():
    inputs = ['古明地觉', '语文', 90], \
             ['古明地觉', '数学', 95], \
             ['古明地觉', '英语', 96], \
             ['芙兰朵露', '语文', 87], \
             ['芙兰朵露', '数学', 92], \
             ['芙兰朵露', '英语', 98],
    data = pd.DataFrame(inputs).rename(columns={0: '姓名', 1: '科目', 2: '分数'})

    two_level_index_series = data.set_index(['姓名', '科目'])['分数']
    res = two_level_index_series.unstack() \
        .rename_axis(columns=None) \
        .reset_index()
    print(res)


def col2row_use_melt():
    inputs = ['1', 13, 21, None], \
             ['2', None, 32, None], \
             ['3', 18, 32, 23]
    data = pd.DataFrame(inputs).rename(columns={0: 'id', 1: 'road1', 2: 'road2', 3: 'road3'})
    print(data)
    print('-' * 30)
    # print(data.iloc[:, 1:].columns.values)

    res = pd.melt(data, id_vars=['id'], value_vars=data.iloc[:, 1:].columns.values, var_name='road', value_name='speed') \
            .dropna(subset=['speed'])
    # res['road'] = res['road'].str.strip('road')  # 去掉road前缀

    print(res)


def col2row_use_wide_to_long():
    # wide_to_long也是引用的melt方法
    inputs = ['1', 12, 21, None], \
             ['2', None, 32, None], \
             ['3', 18, 32, 23]
    data = pd.DataFrame(inputs).rename(columns={0: 'id', 1: 'road1', 2: 'road2', 3: 'road3'})
    print(data)
    print('-' * 30)

    res = pd.wide_to_long(data, stubnames='road', i='id', j='road_id', sep='', suffix=r'\d+') \
        .rename(columns={'road': 'speed'}) \
        .dropna(subset=['speed']) \
        .sort_values(by='id') \
        .reset_index()
    print(res)


def col_split_use_stack():
    inputs = ['琪亚娜·卡斯兰娜', '12月7日', '陶典,钉宫理惠'], \
             ['布洛妮娅·扎伊切克', '8月18日', 'TetraCalyx,Hanser,阿澄佳奈,花泽香菜'], \
             ['德丽莎·阿波卡利斯', '3月28日', '花玲,田村由香里']
    data = pd.DataFrame(inputs).rename(columns={0: '姓名', 1: '生日', 2: '声优'})

    res = data.set_index(['姓名', '生日'])['声优'].str.split(',', expand=True) \
        .stack() \
        .reset_index(drop=True, level=-1) \
        .reset_index() \
        .rename()
    print(res)


def col_split_use_explode():
    inputs = ['琪亚娜·卡斯兰娜', '12月7日', '陶典,钉宫理惠'], \
             ['布洛妮娅·扎伊切克', '8月18日', 'TetraCalyx,Hanser,阿澄佳奈,花泽香菜'], \
             ['德丽莎·阿波卡利斯', '3月28日', '花玲,田村由香里']
    data = pd.DataFrame(inputs).rename(columns={0: '姓名', 1: '生日', 2: '声优'})

    data['声优'] = data['声优'].str.split(',')
    data = data.explode(column='声优') \
        .reset_index()
    print(data)


# https://www.cnblogs.com/traditional/p/11967360.html
if __name__ == '__main__':
    # 行转列
    # row2col_use_pivot()
    # row2col_use_unstack()

    # 列转行
    col2row_use_melt()
    # col2row_use_wide_to_long()

    # 列拆分
    # col_split_use_explode()
    # col_split_use_stack()
