# coding=utf-8
from __future__ import print_function
import os

all_file = []


def get_all_file(path):
    all_file_list = os.listdir(path)
    for f in all_file_list:
        file_path = os.path.join(path, f)
        # 判断是不是文件夹
        if os.path.isdir(file_path):
            get_all_file(file_path)
        all_file.append(file_path)
    return all_file


if __name__ == '__main__':

    src_path = "C:\\he\\py_proj_27\\set_proxy\\code\\default\\python27\\1.0\\lib\\site-packages\\adodbapi"
    allfiles = get_all_file(src_path)

    for item in allfiles:
        print(item)
