import os
import pythoncom
import win32com.shell
from win32com.shell import shell
from win32com.shell import shellcon


def set_shortcut(filename, lnkname, iconname):  # 如无需特别设置图标，则可去掉iconname参数
    shortcut = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink, None,
        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    shortcut.SetPath(filename)
    shortcut.SetIconLocation(iconname, 0)  # 可有可无，没有就默认使用文件本身的图标
    if os.path.splitext(lnkname)[-1] != '.lnk':
        lnkname += ".lnk"
    shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname, 0)


if __name__ == "__main__":
    # 获取"启动"文件夹路径，关键是最后的参数CSIDL_STARTUP，这些参数可以在微软的官方API中找到
    startup_path = shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0, shellcon.CSIDL_STARTUP))
    # 获取"桌面"文件夹路径，将最后的参数换成CSIDL_DESKTOP即可
    desktop_path = shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0, shellcon.CSIDL_DESKTOP))
    file_name = ""  # 要创建快捷方式的文件的完整路径
    icon_name = ""  # 图标文件的完整路径(非必须)
    lnk_name1 = startup_path + "\\我的桌面快捷方式.lnk"  # 将要在此路径创建快捷方式
    lnk_name2 = startup_path + "\\我的启动组快捷方式.lnk"
    set_shortcut(file_name, lnk_name1, icon_name)
    set_shortcut(file_name, lnk_name2, icon_name)
