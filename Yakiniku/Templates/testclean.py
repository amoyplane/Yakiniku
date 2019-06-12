import time
import datetime

import os


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def get_FileAccessTime(filePath):
    filePath = unicode(filePath, 'utf8')
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)


def get_FileCreateTime(filePath):
    filePath = unicode(filePath, 'utf8')
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


def get_FileModifyTime(filePath):
    filePath = unicode(filePath, 'utf8')
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


print(os.getcwd())
now = os.getcwd()
dirs = os.listdir(now)
for file in dirs:
    print(get_FileModifyTime(file))
    print(get_FileCreateTime(file))
    print(get_FileModifyTime(file))
