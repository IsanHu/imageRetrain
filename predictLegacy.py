#-*- coding:utf-8 -*-
from PIL import Image, ImageSequence
import os
import sys
import datetime
from sys import argv
from datetime import datetime
from data_service import DATA_PROVIDER
from Models import ImageModel
import tensorflow as tf
import json

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
        print imgPath
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
                re[human_string] = '%.5f' % score
                if human_string == img.category_name:
                    img.confidence = score
            img.predict_info = json.dumps(re)
            updated_imgs.append(img)
        except:
            print "预测失败"
            continue
    print "更新预测结果"
    if len(updated_imgs) > 0:
    	DATA_PROVIDER.add_images(updated_imgs)

def begin():
    last_id = -1
    images = DATA_PROVIDER.get_next_patch_image(last_id)
    print len(images)
    if len(images) == 0:
        return
    else:
        predict(images)
        last_id = images[-1].id
        print last_id

begin()