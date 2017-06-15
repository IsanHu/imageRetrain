#-*- coding:utf-8 -*-
from PIL import Image, ImageSequence
import os
from io import BytesIO
import sys
import datetime
from sys import argv
from datetime import datetime
from data_service import DATA_PROVIDER
from Models import ImageModel
import tensorflow as tf
import json
from time import sleep

basedir = os.path.abspath(os.path.dirname(__file__))

# Loads label file, strips off carriage return
# 加载标签数据
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile(basedir + '/current_model/retrained_labels.txt')]

# Unpersists graph from file
with tf.gfile.FastGFile(basedir + '/current_model/retrained_graph_20160331.pb', 'rb') as f:
    print("加载模型")
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

sess = tf.Session()
softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

category_dic = {"baoman": 1,"dongman": 2, "food": 3, "pet": 4, "realman": 5, "view": 6}

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
      except (Exception) as e:
        print ("读取图片失败")
        print e.message
        return None
  return image_data


def predict(images):

    imageRootPath = os.path.abspath(os.path.dirname(__file__)) + '/static/images/'
    updated_imgs = []
    for img in images:
        imgPath = os.path.join(imageRootPath, img.path)
        try:
            image_data = read_image2RGBbytesFrom(imgPath)
        except (Exception) as e:
            print "读取图片失败"
            print e.message
            print "continue"
            continue

        try:
            predictions = sess.run(softmax_tensor, \
                         {'DecodeJpeg/contents:0': image_data})
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            re = {}
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                re[human_string] = round(score, 4)
                if human_string == img.category_name():
                    img.confidence = round(score, 4)
            img.predict_info = json.dumps(re)
            img.update_time = datetime.now()
            updated_imgs.append(img)
        except (Exception) as e:
            print "预测失败"
            print e.message
            continue
    print "更新预测结果"
    if len(updated_imgs) > 0:
    	DATA_PROVIDER.add_images(updated_imgs)

def begin():
    count = 0
    last_id = -1

    while(True):
        images = DATA_PROVIDER.get_next_patch_image(last_id)
        image_count = len(images)
        print len(images)
        if len(images) == 0:
            break
        else:
            print "预测%d~%d=====" % (images[0].id, images[-1].id)
            predict(images)
            last_id = images[-1].id
            count = count + image_count
            if count == 90:
                break

    print "总共预测了%d个图片" % count


def saowei():
	images = DATA_PROVIDER.get_unpredict_image(last_id)
    image_count = len(images)
    print len(images)
    if len(images) == 0:
    	return

    print "预测====="
    predict(images)


saowei()


