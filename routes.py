#-*- coding:utf-8 -*-
from flask import jsonify
from flask import render_template
from flask import flash
from flask import current_app
from flask import abort
import datetime
import time
import os
import hashlib
import requests
import json
from StringIO import StringIO
import tensorflow as tf
from PIL import Image, ImageSequence
from io import BytesIO
from werkzeug import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))



def init_route(app):
    print "init routes"



def list_routes(app):
    result = []
    for rt in app.url_map.iter_rules():
        result.append({
            'methods': list(rt.methods),
            'route': str(rt)
        })
    return jsonify({'routes': result, 'total': len(result)})




