# Filename: client.py
# coding:utf-8

import requests
from bqss_text_reader import BQSSTextsReader
import sys
from werkzeug import utils
from urllib import urlretrieve
import uuid
import threading

from io import BytesIO
import os.path

import os


dataFile = sys.argv[1]
imageDir = sys.argv[2]

class ImageDownloader(object):

    @staticmethod
    def filetype(filename):
        filet = filename.rsplit('.', 1)[1]
        if filet is None or len(filet) == 0:
            filet = "gif"
        return filet

    @staticmethod
    def _download_gif(url):
        filename = utils.secure_filename(url)
        filename = imageDir + '/' + str(uuid.uuid4()) + '.' + ImageDownloader.filetype(filename)
        cmd = "/usr/bin/curl" + " " + url + " -o " + filename + ".jpeg"
        print cmd
        try:
            os.system(cmd)
            return filename
        except:
            try:
                os.system(cmd)
                return filename
            except:
                try:
                    os.system(cmd)
                    return filename
                except:
                    return None
        return filename
        

    def __init__(self):
        self.thread_count = 5
        self.textReader = BQSSTextsReader()
        self.textReader.decode_config_file(dataFile)
        self.task_groups = []

    def init_task_groups(self):
        self.task_groups = []
        for ti in range(0, self.thread_count):
            task_group = []
            self.task_groups.append(task_group)

        if len(self.textReader.texts) <= 0:
            print '没有可用url信息'
            return

        group_index = 0
        for i in range(0, len(self.textReader.texts)):
            url = self.textReader.texts[i]
            task_group = self.task_groups[group_index]
            task_group.append(url)
            group_index += 1
            if group_index >= self.thread_count:
                group_index = 0

    @staticmethod
    def download_image_with_task_group(task_group):
        for task in task_group:
            filename = ImageDownloader._download_gif(task)
            if filename is not None:
                print filename

    def do_tasks(self):
        threads = []
        for task_group in self.task_groups:
            th = threading.Thread(target=ImageDownloader.download_image_with_task_group, args=(task_group, ))
            threads.append(th)

        for t in threads:
            t.start()


if __name__ == '__main__':
    downloader = ImageDownloader()
    downloader.init_task_groups()
    downloader.do_tasks()

