#!/usr/bin/python3
"""
a class Client that inherits from BaseModel:
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from os import getenv
from models.base_model import BaseModel, Base

storage_type = getenv("FRUTA_TYPE_STORAGE")


class Client(BaseModel, Base):
    """
    Client class
    """
    __tablename__ = "clients"

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        tel_number = Column(String(60), nullable=True)
        box_left = Column(Integer, nullable=False, default=0)
    else:
        name = ''
        tel_number = ''
        box_left = 0