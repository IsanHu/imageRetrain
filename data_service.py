#-*- coding:utf-8 -*-
# coding=utf8
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy import func
import time
import datetime
import sys
import math
import global_config

from Models import ImageModel
from Models import init_database

category_dic_id = {"baoman":1, "dongman": 2, "food":3, "pet":4, "realman":5, "view": 6}
category_dic_readable_id = {"暴漫":1, "动漫": 2, "美食":3, "萌宠":4, "真人":5, "美景": 6}

per_page = 20
class DataService:
    def __init__(self, engine):
        """
        :param engine: The engine route and login details
        :return: a new instance of DAL class
        :type engine: string
        """
        if not engine:
            raise ValueError('The values specified in engine parameter has to be supported by SQLAlchemy')
        self.engine = engine
        db_engine = create_engine(engine, isolation_level="READ UNCOMMITTED")
        db_session = sessionmaker(bind=db_engine)
        self.session = db_session()
        print 'init DataProviderService'

    def init_database(self):
        """
        Initializes the database tables and relationships
        :return: None
        """
        init_database(self.engine)



    def add_images(self, images):
        for img in images:
            self.session.add(img)
        self.session.commit()

    def get_next_patch_image(self, latestId, serialize=False):
        try:
            images = self.session.query(ImageModel).filter(ImageModel.confidence == 0, ImageModel.id > latestId).limit(100).all()
            if serialize:
                return [img.mini_serialize() for img in images]
            else:
                return images
        except (Exception) as e:
            print "抓到exception"
            print "get_next_patch_image"
            print e.message
            return []

    def get_unpredict_image(self, serialize=False):
        try:
            images = self.session.query(ImageModel).filter(ImageModel.confidence == 0, ImageModel.predict_info =="").all()
            if serialize:
                return [img.mini_serialize() for img in images]
            else:
                return images
        except (Exception) as e:
            print "抓到exception"
            print "get_next_patch_image"
            print e.message
            return []

    def image_count_of_category(self, category_id):
        count = self.session.query(ImageModel).filter(ImageModel.category == category_id and ImageModel.status != -1).count()
        return count

    def images_at_page(self, page=1, category="类别", confidence=-1, grater=1, checked=-1, serialize=False):
        try:
            offset = (page - 1) * per_page

            imagesQuery = self.session.query(ImageModel)
            imagesQuery.filter(ImageModel.status != -1)

            if category_dic_readable_id.has_key(category):
                category_id = category_dic_readable_id[category]
                imagesQuery = imagesQuery.filter(ImageModel.category == category_id)

            if checked != -1:
                imagesQuery = imagesQuery.filter(ImageModel.status == checked)

            if confidence != -1:
                if grater == 1:
                    imagesQuery = imagesQuery.filter(ImageModel.confidence >= confidence)
                else:
                    imagesQuery = imagesQuery.filter(ImageModel.confidence <= confidence)

            count = imagesQuery.count()
            page_count = int(math.ceil(count / float(per_page)))
            print page_count
            if page_count == 0:
                page_count = 1

            page_indexs = [(i + 1) for i in range(page_count)]
            current_page = page

            images = imagesQuery.order_by(ImageModel.confidence.desc()).offset(offset).limit(per_page).all()
            if serialize:
                return [img.serialize() for img in images], page_indexs, current_page
            else:
                return images, page_indexs, current_page
        except (Exception) as e:
            print "抓到exception"
            print "images_at_page 操作失败"
            print e.message
            return [], [], 1


    def confirm_images_with_ids(self, image_ids):
        try:
            images = []
            for img_id in image_ids:
                imgs = self.session.query(ImageModel).filter(ImageModel.id == img_id).limit(1).all()
                if len(imgs) == 1:
                    images.append(imgs[0])
        except (Exception) as e:
            print "查询出所有要操作的数据失败: "
            print e.message
            return {"result": 0, "error_message": "查询出所有要操作的数据失败: %s" % e.message}
        try:
            for img in images:
                img.status = 1
            for img in images:
                self.session.add(img)

            self.session.commit()
        except (Exception) as e:
            print "更新图片状态失败: %s" % e.message
            return {"result": 0, "error_message": "更新图片状态失败: %s" % e.message}

        return {"result": 1, "message": "更新成功 %d 张图片" % len(images)}


    def remove_images_with_ids(self, image_ids):
        try:
            images = []
            for img_id in image_ids:
                imgs = self.session.query(ImageModel).filter(ImageModel.id == img_id).limit(1).all()
                if len(imgs) == 1:
                    images.append(imgs[0])
        except (Exception) as e:
            print "查询出所有要操作的数据失败: "
            print e.message
            return {"result": 0, "error_message": "查询出所有要操作的数据失败: %s" % e.message}
        try:
            for img in images:
                img.status = -1
            for img in images:
                self.session.add(img)

            self.session.commit()
        except (Exception) as e:
            print "更新图片状态失败: %s" % e.message
            return {"result": 0, "error_message": "更新图片状态失败: %s" % e.message}

        return {"result": 1, "message": "更新成功 %d 张图片" % len(images)}





    def testFilter(self):
        countQuery = self.session.query(ImageModel)
        countQuery = countQuery.filter(ImageModel.category == 1)
        countQuery = countQuery.filter(ImageModel.confidence > 0.9)
        count = countQuery.count()

        images = countQuery.order_by(ImageModel.confidence.desc()).limit(10).all()

        return count, images





DATA_PROVIDER = DataService(global_config.config['db_engine'])

