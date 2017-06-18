# Filename: client.py
# coding:utf-8

import requests
from bqss_text_reader import BQSSTextsReader

from werkzeug import utils
from urllib import urlretrieve
import uuid
import threading
import os
import mechanize
from sys import argv
import hashlib

br = mechanize.Browser()

urlFile = argv[1]
outFodler = argv[2]

downloadedUrls = []
urls = []


def md5_name(name):
    m = hashlib.md5()
    m.update(name)
    return m.hexdigest()



with open(urlFile, 'r') as f:
    for line in f.readlines():
        line_str = line.strip()
        # url = utils.secure_filename(line_str)
        urls.append(line_str)

for url in urls:
    extension = url.rsplit('.', 1)[1]
    print extension
    hash_name = md5_name(url)

    # urlretrieve(url, filename)
    cmd = "/usr/bin/curl" + " " + url + " -o " + outFodler + "/" + hash_name + "." + extension
    print cmd
    try:
        os.system(cmd)
    except (Exception) as e:
        print url
        print "下载失败"

