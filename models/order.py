#!/usr/bin/python3
"""
a class Order that inherits from BaseModel:
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import models
from os import getenv






class Order(BaseModel, Base):
    """
    Order class
    """
    if models.StorageType == "db":
        __tablename__ = "orders"
        quantity = Column(Float,nullable=False)
        total_price = Column(Float,nullable=False)
        client_id = Column(String(60), ForeignKey("clients.id"), nullable=False)
        product_id = Column(String(60), ForeignKey("products.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        boxes_number = Column(Integer, default=0, nullable=False)


    else:
        client_id = ''
        product_id = ''
        quantity = 0
        total_price = 0
        user_id = ''
        boxes_number = ''

