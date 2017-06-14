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
unqualifiedDir = sys.argv[3]

print(candidateImgDir)
print(trashImgDir)
print(unqualifiedDir)

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

# 加载标签数据
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("./retrained_labels.txt")]

# Unpersists graph from file
# 从文件中读取重新训练好的模型
with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


result = []
with tf.Session() as sess:
  trashFile = open("trash.txt", "wb")
  unqualifiedFile = open("unqualified.txt", "wb")
  index = 0
  list_dirs = os.walk(candidateImgDir) 
  for root, dirs, files in list_dirs:  
      for f in files: 
        index = index + 1
        if index < 3000:
          continue
        imagePath = os.path.join(root, f)
        trashPath = trashImgDir + f
        unqualifiedPath = unqualifiedDir + f
        image_data = read_image2RGBbytesFrom(imagePath)
        if image_data is None:
          print ("读取图片失败")
          cmd = "cp " + imagePath + " " + trashPath
          os.system(cmd)
          trashFile.write(f + "\n")
          print cmd
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
            if human_string == "pet":
               result.append({"imagePath": imagePath, "r":'%.5f' % score})
               if score < 0.45:
                  cmd = "cp " + imagePath + " " + unqualifiedPath
                  unqualifiedFile.write(f + "\n")
                  os.system(cmd)
                  print(cmd)

                 

        if index % 20 == 0:
          print(str(index) + ' 个图片已被处理')

  unqualifiedFile.close()
  trashFile.close()
        
def score(s): 
   return s['r'] 
# 遍历数组排序
sortedResult = sorted(result,key = score)

resultString = json.dumps(sortedResult)
fo = open("result.txt", "wb")
fo.write(resultString);
fo.close()