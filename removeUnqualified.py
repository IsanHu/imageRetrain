#-*- coding:utf-8 -*-
import sys
from PIL import Image, ImageSequence
from io import BytesIO
import os.path
import requests
from StringIO import StringIO
import json
import os

ImgDir = sys.argv[1]
bottleneckDir = sys.argv[2]
trashFileName = sys.argv[3]
print(trashFileName) 

## 读取文件
trashFileNames = []
trashFile = open(trashFileName)
line = trashFile.readline()             # 调用文件的 readline()方法
while line:
    trashFileNames.append(line)
    line = trashFile.readline()
trashFile.close()



for name in trashFileNames:
	stripedName = name.strip()
	cmd = "rm " + ImgDir + stripedName
	os.system(cmd)
	print(cmd)
	cmd1 = "rm " + bottleneckDir + stripedName + ".txt"
	os.system(cmd1)
	print(cmd1)