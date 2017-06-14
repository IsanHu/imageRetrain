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

db_engine = create_engine(global_config.config['db_engine'], isolation_level="READ UNCOMMITTED")
session_factory = sessionmaker(bind=db_engine)
Scope_Session = scoped_session(session_factory)

per_page = 10

class DataService:
    def __init__(self, engine):
        """
        :param engine: The engine route and login details
        :return: a new instance of DAL class
        :type engine: string
        """
        if not engine:
            raise ValueError('The values specified in engine parameter has to be supported by SQLAlchemy')
        print 'init DataService'

    def init_database(self):
        """
        Initializes the database tables and relationships
        :return: None
        """
        init_database(self.engine)


    def add_images(self, images):
        temp_session = Scope_Session()
        for img in images:
            temp_session.add(img)
        temp_session.commit()
        Scope_Session.remove()



DATA_PROVIDER = DataService(global_config.config['db_engine'])

