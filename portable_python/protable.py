import os
import shutil


def visitDirFile(dir, visitor):
    """递归访问目录及其子目录下的文件"""
    assert (os.path.isdir(dir)), dir
    for i in os.listdir(dir):
        fullPathName = os.path.join(dir, i)
        if os.path.isfile(fullPathName):
            if visitor(fullPathName):
                return True
        elif os.path.isdir(fullPathName):
            # 访问子目录
            if visitDirFile(fullPathName, visitor):
                return True


def findPyFile(file):
    """查找相应的Py文件(不考虑pyo文件)"""
    if file[-4:] == '.pyc':
        # 得到编译文件对应的源文件
        dir = os.path.dirname(file)
        if dir.endswith('__pycache__'):
            dir = dir[:-11]
        # 文件中可能有点存在,要排除3.2之后的缓存
        name, ext = os.path.splitext(os.path.basename(file))
        name2, ext = os.path.splitext(name)
        if ext.startswith('.cpython'):
            name = name2
        srcFile = os.path.join(dir, '%s.py' % name)
        # 源文件可能是pyw文件
        if not os.path.isfile(srcFile):
            srcFile += 'w'
        destFile = srcFile.replace(srcDir, destDir)
        print(srcFile)
        # 保证目标目录存在
        dir = os.path.dirname(destFile)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        # 拷贝文件及状态
        shutil.copy2(srcFile, destFile)


if __name__ == '__main__':
    import sys

    srcDir = "C:\\Users\\heyon\\AppData\\Local\\Programs\\Python\\Python36"
    destDir = os.path.join("D\\python36", 'miniPython')
    visitDirFile(srcDir, findPyFile)
