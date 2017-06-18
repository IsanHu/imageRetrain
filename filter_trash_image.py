#-*- coding:utf-8 -*-
import tensorflow as tf, sys
from PIL import Image, ImageSequence
from io import BytesIO
import os.path
import requests
from StringIO import StringIO
import json
import os

candidateImgDir = sys.argv[1]
trashImgDir = sys.argv[2]


def read_image2RGBbytesFrom(image_path):
  with BytesIO() as output:
      try:
        with Image.open(image_path) as img:
          frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
          frameCount = len(frames)
          if frameCount < 5 :
              temImg = frames[frameCount // 2]
              temImg.convert('RGB').save(output, 'JPEG')
          else:
              temImg = frames[frameCount - 4]
              temImg.convert('RGB').save(output, 'JPEG')
          image_data = output.getvalue()
      except:
        print ("读取图片失败")
        return None
  return image_data



for f in os.listdir(candidateImgDir):  
	path = candidateImgDir + "/" + f
	image_data = read_image2RGBbytesFrom(path)
        if image_data is None:
          print ("读取图片失败")
          cmd = "mv " + path + " " + trashImgDir + "/" + f
          os.system(cmd)
          print cmd
          continue		
        else:
        	print "ok"


