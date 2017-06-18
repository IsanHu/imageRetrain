#-*- coding:utf-8 -*-
from sqlalchemy import Column, String, Integer,Float, ForeignKey, Numeric, Date
from Model import Model
import json
import os
import time
from datetime import date, datetime

category_dic = {1: "baoman", 2: "dongman", 3: "food", 4: "pet", 5: "realman", 6: "view"}

class ImageModel(Model):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, nullable=False)
    path = Column(String(100), nullable=False, default='')
    size = Column(Integer, nullable=False, default=0)
    width = Column(Integer, nullable=False, default=0)
    height = Column(Integer, nullable=False, default=0)
    category = Column(Integer, nullable=False, default=0)
    confidence = Column(Float, nullable=True, default=0)
    predict_info = Column(String(1024), nullable=True, default='')
    checked = Column(Integer, nullable=False, default=0)
    ahash8 = Column(String(1024), nullable=False, default='')
    ahash16 = Column(String(1024), nullable=False, default='')
    update_time = Column(Date, nullable=False)
    status = Column(Integer, nullable=False, default=0)

    @classmethod
    def get_new_instance(cls, img):
        new_img = ImageModel(id=img.id,
                             path=img.path,
                             size=img.size,
                             width=img.width,
                             height=img.height,
                             category=img.category,
                             confidence=img.confidence,
                             predict_info=img.predict_info,
                             checked=img.checked,
                             ahash8=img.ahash8,
                             ahash16=img.ahash16,
                             update_time=img.update_time,
                             status=img.status,
                       )
        return new_img

    def serialize(self):
        return {
            "id": self.id,
            "path": "/images/" + self.path,
            "size": self.size,
            "width": self.width,
            "height": self.height,
            "category": self.category_name(),
            "confidence": self.confidence,
            "predict_info": json.loads(self.predict_info),
            "checked": self.checked,
            "ahash8":self.ahash8,
            "ahash16":self.ahash16,
            "update_time": str(self.update_time),
            "status": self.status,
        }

    def category_name(self):
        return category_dic[self.category]


