import subprocess
import os

curr_path = os.getcwd()
data_file_path = curr_path+"\\data"
status = os.path.exists(data_file_path)
print(status)
if not status:
    data_file = open(data_file_path, "w")
    data_file.close()
    subprocess.call(["Wscript.exe", "//E:JScript", "create_shortcut.js"], shell=False)
