#!/usr/bin/python3
"""
a class Order that inherits from BaseModel:
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models.product import Product
import models
from os import getenv






class Order(BaseModel, Base):
    """
    Order class
    """
    __tablename__ = "orders"
    if models.StorageType == "db":

        client_id = Column(String(60), ForeignKey("clients.id"), nullable=False)
        product_id =Column(String(60), ForeignKey("products.id"), nullable=False)
        quantity = Column(Float,nullable=False)
        total_price = Column(Float,nullable=False)





    else:
        client_id = ''
        product_id = ''
        quantity = 0
        total_price = 0


