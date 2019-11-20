import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
# server_file = r"C:\he\set_proxy 副本\code\default\launcher\start_brook.cmd"
server_file = current_path + "\\start_brook.cmd"
server = ""
pwd = ""
try:
    with open(server_file, mode='r') as server_file:  # , py2中没有encoding='utf-8'
        # server = server_file.read()
        server = server_file.readline().strip()
        pwd = server_file.readline()
except:
    # logging.error()
    sys.exit(0)
print("server:"+server+"pwd:"+pwd)
