# coding=utf-8

import os
import glob
import sys

all_file = []
all_dir = []


def get_all_files(path):
    global all_file
    global all_dir
    for dirpath, dirnames, filenames in os.walk(path):
        for d in dirnames:
            all_dir.append(os.path.join(dirpath, d))
        for name in filenames:
            all_file.append(os.path.join(dirpath, name))
            if name.endswith('.pyc'):
                print(name)
                os.remove(os.path.join(dirpath, name))


if __name__ == '__main__':
    path = "D:\\soft\\agent\\set_proxy\\code\\default"
    get_all_files(path)
    # for f in all_file:
    #     print(f)
    # print(len(all_file))
    # print(dir_list)
    # print(file_list)




