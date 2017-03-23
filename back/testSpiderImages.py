#-*- coding:utf-8 -*-
import tensorflow as tf, sys
from PIL import Image, ImageSequence
from io import BytesIO
import os.path
import requests
from StringIO import StringIO
import json


def read_image2RGBbytesFrom(response):
  with BytesIO() as output:
    
      try:
        with Image.open(StringIO(response.content)) as img:
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

# 加载标签数据
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("./retrained_labels.txt")]

## 读取文件
imageUrls = []
f = open("./spider.txt")             # 返回一个文件对象
line = f.readline()             # 调用文件的 readline()方法
while line:
    imageUrls.append(line)
    line = f.readline()
f.close()

# Unpersists graph from file
# 从文件中读取重新训练好的模型
with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


result = []
with tf.Session() as sess:
  logFile = open("log.txt", "wb")
  index = 0
  for url in imageUrls:
    print (index)
    print (url)
    #读取输入图片数据
    try:
      response = requests.get(url)
    except:
      print ("下载失败")
      print (r)
      continue

    image_data = read_image2RGBbytesFrom(response)
    if image_data is None:
      print ("读取图片失败")
      continue

    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})
    
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        if human_string == "good":
           logFile.write(json.dumps({"url": url, "r":'%.5f' % score}))
           result.append({"url": url, "r":'%.5f' % score})
    index = index + 1

  logFile.close()
        


resultString = json.dumps(result)
fo = open("result.txt", "wb")
fo.write(resultString);
fo.close()
