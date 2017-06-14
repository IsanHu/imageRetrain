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
            images = self.session.query(ImageModel).filter(ImageModel.confidence != 0, ImageModel.id > 46860).all()
            # clean_images = [ImageModel.get_new_instance(img) for img in images]
            if serialize:
                return [img.mini_serialize() for img in images]
            else:
                return images
        except (Exception) as e:
            print "抓到exception"
            print "get_next_patch_image"
            print e.message
            return [], [], 1



DATA_PROVIDER = DataService(global_config.config['db_engine'])

