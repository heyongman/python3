import sys
import os
server = None

if not server:
    print("获取Server信息失败！")
    # sys.exit(0)

c_dir = os.path.dirname(os.path.abspath(__file__))
start_file = c_dir + "\\start_brook.cmd"
print(start_file)

new_line = "ghjhgh67898"
with open(start_file, encoding='utf-8', mode='w') as f:
    f.write(new_line)
