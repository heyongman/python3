import os
import os.path


def DeleteFiles(path, fileList):
    for parent, dirnames, filenames in os.walk(path):

        FullPathList = []
        DestPathList = []

        for x in fileList:
            DestPath = path + x
            DestPathList.append(DestPath)

        for filename in filenames:
            FullPath = os.path.join(parent, filename)
            FullPathList.append(FullPath)

        for xlist in FullPathList:
            if xlist not in DestPathList:
                os.remove(xlist)


src = "C:\\he\\py_proj_27\\set_proxy\\code\\default\\python27\\1.0\\lib"
sl = "distutils"
is_dir = os.path.isdir(os.path.join(src, sl))
print(is_dir)
