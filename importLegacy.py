#-*- coding:utf-8 -*-
from PIL import Image, ImageSequence
import os
import sys
import datetime
from sys import argv
import imagehash
from datetime import datetime
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

category_id = category_dic[category]
errror_imgs = []
def begin():
	index = 0
	imgs = []
	files = os.listdir(categoryPath)
	print '总共有%d文件' % len(files)
	for f in files:
		rePath = category + "/" + f
		if allowed_file(f):
			try:
				filePath = os.path.join(categoryPath, f)
				img = Image.open(filePath)
				width = img.size[0]
				height = img.size[1]

				ratio = float(width) / float(height)
				if ratio > 2 or ratio < 0.5:
					print "%s ratio不合理: %f" % (f, ratio)
					errror_imgs.append(rePath)
					continue


				size = os.path.getsize(filePath) / 1024

				ahash8 = imagehash.average_hash(img,8)
				ahashString8 = ahash8.__str__()

				ahash16 = imagehash.average_hash(img,16)
				ahashString16 = ahash16.__str__()

				imgModel = ImageModel(path=rePath,
									  size=size,
									  width=width,
									  height=height,
									  category=category_id,
									  ahash8=ahashString8,
									  ahash16=ahashString16,
									  update_time=datetime.now())
				imgs.append(imgModel)

			except (Exception) as e:
				print "处理 %s 出错" % rePath
				errror_imgs.append(rePath)
				print e.message
				continue

			index = index + 1
			try:
				## 每10个插入一次数据
				if index % 10 == 0:
					DATA_PROVIDER.add_images(imgs)
					imgs = []
					print "插入数据: %d ~ %d" % (index - len(imgs), index)
			except (Exception) as e:
				print "插入数据失败: %d ~ %d" % (index - len(imgs), index)
				for img in imgs:
					errror_imgs.append(img.path)
				imgs = []
		else:
			print "%s 文件类型不对" % f
			errror_imgs.append(rePath)

	try:
		print "插入最后%d个数据" % len(imgs)
		DATA_PROVIDER.add_images(imgs)
	except (Exception) as e:
		print "插入最后%d个数据出错" % len(imgs)
		for img in imgs:
			errror_imgs.append(img.path)

	print "总共有%d个数据处理失败" % len(errror_imgs)
	print errror_imgs

	print "开始删除处理失败的数据========="

	for img in errror_imgs:
		img_path = os.path.join(imageRootPath, "/" + img)
		try:
			cmd = "rm " + img_path
			os.system(cmd)
		except (Exception) as e:
			print "删除%s失败" % img

	files = os.listdir(categoryPath)
	print "有效数据: %d" % len(files)




begin()

