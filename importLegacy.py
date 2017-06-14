#-*- coding:utf-8 -*-
from PIL import Image, ImageSequence
import os
import sys
import datetime
from sys import argv
import imagehash

from data_service import DATA_PROVIDER
from Models import ImageModel


ALLOWED_EXTENSIONS = set(['gif', 'GIF', 'jpg', 'JPG', 'jpeg', 'JPEG'])
IGNORED_FILES = set(['.gitignore', '.DS_Store'])

category_dic = {"baoman": 1,"dongman": 2, "food": 3, "pet": 4, "realman": 5, "view": 6}

def allowed_file(filename):
    return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS			

imageRootPath = os.path.abspath(os.path.dirname(__file__)) + '/static/images/'
category = argv[1]
categoryPath = os.path.join(imageRootPath, category)


def begin():
	index = 0
	for f in sorted(os.listdir(categoryPath)):
		if allowed_file(f):
			rePath = category + "/" + f
			print rePath

			filePath = os.path.join(categoryPath, f)
			size = os.path.getsize(filePath) / 1024
			print 'size : %d' % size


			img = Image.open(filePath)
			width = img.size[0]
			height = img.size[1]
			print width
			print height

			ahash8 = imagehash.average_hash(img,8)
			ahashString8 = ahash8.__str__()

			ahash16 = imagehash.average_hash(img,16)
			ahashString16 = ahash16.__str__()


			index = index + 1
			## 每10个插入一次数据
			if index % 10 == 0:
				print "插入数据: %d ~ %d" % (index - 10, index)

			if index > 10:
				return

		else:
			print "%s 文件类型不对" % f


begin()

