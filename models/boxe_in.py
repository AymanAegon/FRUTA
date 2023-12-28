#!/usr/bin/python3
"""
a class Order that inherits from BaseModel:
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import models
from os import getenv






class Boxe_in(BaseModel, Base):
    """
    Boxe_in class
    """
    if models.StorageType == "db":
        __tablename__ = "boxes_in"
        client_id = Column(String(60), ForeignKey("clients.id"), nullable=False)
        boxes_number = Column(Integer, default=0, nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
