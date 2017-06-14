# coding:utf-8
import os
import sys
from PIL import Image, ImageSequence


originalImgDir = sys.argv[1]
# longImgDir = sys.argv[2]



list_dirs = os.walk(originalImgDir) 
for root, dirs, files in list_dirs:  
    for f in files: 
    	try:
		originalPath = os.path.join(root, f)
		img = Image.open(originalPath)
		print(img.verify())
    	except:
		print ("处理" + f + "失败")