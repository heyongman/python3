import xlrd
import pandas as pd
import numpy as np

pd.set_option('display.min_rows', 20)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


def device_turning():
    # inter_id,entrance_id,bayonet_id,road_id
    joined = pd.read_excel(r'D:\文档\项目\贵阳TOCC\数据采集接口\交管局\卡口-渠化-道路-修正20200907.xlsx',
                           sheet_name='关联上的卡口', skiprows=1, dtype=object)
    cols = np.append(['kk_id', 'inter_id'], joined.iloc[:, 10:].columns.values)
    joined = joined[cols].rename(columns={'kk_id': 'device_no'})

    # unjoined = pd.read_excel(r'D:\文档\项目\贵阳TOCC\数据采集接口\交管局\卡口-渠化-道路-修正20200907.xlsx',
    #                          sheet_name='未关联上的卡口', skiprows=1, dtype=object)
    # cols = np.append(['未关联上的卡口', 'DIRECTION'], unjoined.iloc[:, 13:].columns.values)
    # unjoined = unjoined[cols].rename(columns={'未关联上的卡口': 'device_no', 'DIRECTION': 'inter_id'})
    # data = pd.concat([joined, unjoined]).dropna(subset=['device_no'])
    data = joined.dropna(subset=['device_no'])

    res = pd.melt(data, id_vars=['device_no', 'inter_id'], value_vars=data.iloc[:, 2:].columns.values, var_name='car_road', value_name='turning') \
        .dropna(subset=['turning'])

    res['car_road'] = res['car_road'].str.strip('车道')
    res['turning'] = res['turning']\
        .replace(['查不到', '拆除', '施工拆除', '转盘'], None)\
        .replace('2、4',11)\
        .replace('4、3',12)
    print(res)

    # res.to_excel(r'D:\文档\项目\贵阳TOCC\数据采集接口\交管局\卡口-渠化-道路-修正-列转行.xlsx', index=None)
    res.to_csv(r'D:\文档\项目\贵阳TOCC\数据采集接口\交管局\卡口-渠化-道路-修正-列转行.csv',sep='\t',header=False,index=False)


if __name__ == '__main__':
    device_turning()
