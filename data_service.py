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
        count = self.session.query(ImageModel).filter(ImageModel.category == category_id).count()
        return count

    # def images_at_page(self, page=1, confidence=-1, moreConfident=True, checked=-1, serialize=False):
    #     try:
    #         offset = (page - 1) * per_page
    #
    #         countQuery = self.session.query(ImageModel)
    #         imagesQuery = self.session.query(ImageModel)
    #
    #         if checked != -1:
    #             countQuery.filter
    #
    #
    #         if confidence == -1:
    #
    #
    #
    #
    #         count = self.session.query(ImageModel).filter(ImageModel. != -1, Video.name.like('%' + key + '%')).count()
    #         page_count = int(math.ceil(count / float(per_page)))
    #         print page_count
    #         if page_count == 0:
    #             page_count = 1
    #
    #         page_indexs = [(i + 1) for i in range(page_count)]
    #         current_page = page
    #
    #         videos = temp_session.query(Video).filter(Video.status != -1, Video.name.like('%' + key + '%')).order_by(
    #             Video.upload_time.desc()).offset(offset).limit(per_page)
    #         clean_videos = [Video.get_new_instance(vi) for vi in videos]
    #         Scope_Session.remove()
    #         if serialize:
    #             return [vi.mini_serialize() for vi in clean_videos], page_indexs, current_page
    #         else:
    #             return clean_videos, page_indexs, current_page
    #     except (Exception) as e:
    #         print "抓到exception"
    #         print "all_videos 操作失败"
    #         print e.message
    #         return [], [], 1

    def testFilter(self):
        countQuery = self.session.query(ImageModel)
        countQuery = countQuery.filter(ImageModel.category == 1)
        countQuery = countQuery.filter(ImageModel.confidence > 0.9)
        count = countQuery.count()

        images = countQuery.order_by(ImageModel.confidence.desc()).limit(10)

        return count, images





DATA_PROVIDER = DataService(global_config.config['db_engine'])

