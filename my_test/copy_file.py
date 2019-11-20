"""
将目录下的ogg音频文件合并为一个文件
"""
import os
from pydub import AudioSegment

sour_dir = "D:\\Android\\res"
sour_list = os.listdir(sour_dir)

res = AudioSegment.empty()
# 打开文件，获取内容
for file_list in sour_list:
    sound = AudioSegment.from_file("D:\\Android\\res\\" + file_list, format="ogg")
    res += sound
# 写入文件
file_handle = res.export("D:\\Android\\res.ogg", format="ogg")
