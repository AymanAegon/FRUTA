#!/usr/bin/python3
"""
a class Product that inherits from BaseModel:
"""
from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship
from os import getenv
from models.base_model import BaseModel, Base
import models



class Product(BaseModel, Base):
    """
    Product class
    """
    if models.StorageType == 'db':
        __tablename__ = "products"
        name = Column(String(128), nullable=False)
        unit_price = Column(Float, nullable=False)
        unit_name = Column(String(128), nullable=True, default="unit")
        stock = Column(String(128), nullable=False, default=0)
       
    else:
        name = ''
        unit_price = 0
        unit_name = "unit"
        stock = 0