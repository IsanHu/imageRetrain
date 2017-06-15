#-*- coding:utf-8 -*-
from PIL import Image, ImageSequence
import os
import sys
import datetime
from sys import argv
from datetime import datetime
from data_service import DATA_PROVIDER
from Models import ImageModel


category_dic = {"baoman": 1,"dongman": 2, "food": 3, "pet": 4, "realman": 5, "view": 6}
imageRootPath = os.path.abspath(os.path.dirname(__file__)) + '/static/images/'
print imageRootPath




for (key, value) in category_dic.items():
    db_count = DATA_PROVIDER.image_count_of_category(value)
    print "%s 在数据库中有%d个图片" % (key, db_count)

    categoryPath = os.path.join(imageRootPath, key)
    files = os.listdir(categoryPath)
    disk_count = len(files)
    print "%s 在磁盘中有%d个图片" % (key, disk_count)
    if disk_count != db_count:
        print "%s 在数据库中和在磁盘中的图片数量不一样" % key

