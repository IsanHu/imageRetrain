#-*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap
from routes import init_route
# import cv2
import simplejson
import numpy as np
from PIL import Image, ImageSequence
import os
import sys
import requests
from StringIO import StringIO
import datetime
from sys import argv

from data_service import DATA_PROVIDER
from Models import ImageModel


reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

bootstrap = Bootstrap(app)


init_route(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', tab='upload')

@app.route("/images", methods=['POST'])
def get_images_at_page():
    params = request.form
    page = int(params['page'])
    category = params['category'].encode('utf-8')
    confidence = float(params['confidence'])
    checked = int(params['checked'])
    greater = int(params['greater'])

    images, page_indexs, current_page = DATA_PROVIDER.images_at_page(page=page, category=category, confidence=confidence,grater=greater,checked=checked,serialize=True)
    return simplejson.dumps({"images":images, "page_indexs":page_indexs, "current_page": current_page})

@app.route("/confirm_images", methods=['POST'])
def confirm_images():
    params = request.form
    image_ids = params['image_ids']
    print image_ids
    result = DATA_PROVIDER.confirm_images_with_ids(image_ids)
    return simplejson.dumps(result)


if __name__ == "__main__":
    port = argv[1]
    app.run(host='0.0.0.0', port=port)


