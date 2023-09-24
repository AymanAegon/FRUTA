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
    __tablename__ = "boxs"
    if storage_type == 'db':
        number = Column(Integer, nullable=False, default=0)
    else:
        number = 0