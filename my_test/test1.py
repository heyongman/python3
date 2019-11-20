import pandas as pd
import xlrd


def read_file(f_list, sheet_name):
    global frames_result
    frames = []
    for i in range(len(f_list)):
        fe = open('D:\\大数据视频\\1036、10小时入门大数据\\新建 Microsoft Excel 工作表.xlsx', 'rb')
        file = pd.read_excel(fe, sheet_name)
        frames.append(file)
        frames_result = pd.concat(frames)
    return frames_result


file_list = [1]
file_inner = read_file(file_list, 'Sheet1')
# file_outer = read_file(file_list, 'APP外事件埋点')
# file_activity = read_file(file_list, '活动页面')
# file_king = read_file(file_list, '龙虎榜PV')
print(file_inner)
