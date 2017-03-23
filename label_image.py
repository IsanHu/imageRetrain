#-*- coding:utf-8 -*-
import tensorflow as tf, sys
from PIL import Image, ImageSequence
from io import BytesIO
import os.path


# change this as you see fit
image_path = sys.argv[1]



# Read in the image_data
# image_data = tf.gfile.FastGFile(image_path, 'rb').read()

def read_image2RGBbytes(image_path):
  jpgext = ['.jpg', '.jpeg', '.JPG', '.JPEG']
  print (image_path)
  # if (os.path.splitext(image_path)[1] in jpgext):
  #   image_data = gfile.FastGFile(image_path, 'rb').read()
  # else:
  with BytesIO() as output:
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
  return image_data


#读取输入图片数据
image_data = read_image2RGBbytes(image_path)



# Loads label file, strips off carriage return
# 加载标签数据
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("./retrained_labels.txt")]

# Unpersists graph from file
# 从文件中读取重新训练好的模型
with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})
    
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        print('%s (score = %.5f)' % (human_string, score))