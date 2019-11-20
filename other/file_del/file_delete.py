# coding=utf-8
"""
删除目录中非‘VO.bytes’结尾的文件
"""
import re
import os
import shutil

delDir = "D:\\Android"
delList = os.listdir(delDir)

for f in delList:
    # print(f)
    reg = re.compile('VO.bytes$')
    res = re.search(reg, f)
    if not res:
        filePath = os.path.join(delDir, f)
        if os.path.isfile(filePath):
            os.remove(filePath)
            print(filePath + " was removed!")
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath, True)
            print("Directory: " + filePath + " was removed!")
