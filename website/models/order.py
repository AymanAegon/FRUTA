#!/usr/bin/python3
"""
a class Order that inherits from BaseModel:
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models.client import Client
from models.product import Product
from models.box import Box
from os import getenv



storage_type = getenv("FRUTA_TYPE_STORAGE")






class Order(BaseModel, Base):
    """
    Order class
    """
    __tablename__ = "orders"
    if storage_type == "db":

        client_id = Column(String(60), ForeignKey("clients.id"), nullable=False)
        product_id =Column(String(60), ForeignKey("products.id"), nullable=False)
        quantity = Column(Float,nullable=False)
        total_price = Column(Float,nullable=False)
        box_out = Column(Integer,primary_keys=True,nullable=False)
        box_in = Column(Integer,primary_keys=True,nullable=False)

        boxes_out = relationship("Boxes_out", backref="order")
        boxes_in = relationship("Boxes_in", backref="order")


    else:
        client_id = ''
        product_id = ''
        quantity = 0
        total_price = 0
        box_out = 0

