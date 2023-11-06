#!/usr/bin/python3
"""
a class Box that inherits from BaseModel:
"""
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from os import getenv
from models.base_model import BaseModel, Base

storage_type = getenv("FRUTA_TYPE_STORAGE")


class Box(BaseModel, Base):
    """
    Box class
    """
    __tablename__ = "boxes"
    if storage_type == 'db':
        box_left = Column(Integer, nullable=True, default=0)
        box_by_order= Column(Integer, nullable=True, default=0)
        box_by_client = Column(Integer, nullable=True, default=0)
    else:
        box_left = 0
        box_by_order = 0
        box_by_client = 0