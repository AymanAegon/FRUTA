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
        number_box = Column(Integer,nullable=False)
    else:
        client_id = ''
        product_id = ''
        quantity = 0
        total_price = 0
        number_box = 0

