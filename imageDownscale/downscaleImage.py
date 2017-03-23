# coding:utf-8

import os
import sys


originalImgDir = sys.argv[1]
processedImgDir = sys.argv[2]



list_dirs = os.walk(originalImgDir) 
for root, dirs, files in list_dirs:  
    for f in files: 
    	try:
		cmd = "/usr/local/bin/gifsicle " + os.path.join(root, f) + " --resize-fit 240x240 -O3 -lossy=90 -o " + processedImgDir + f
		print cmd
		os.system(cmd)
		print f
    	except:
    		print ("处理" + f + "失败")
