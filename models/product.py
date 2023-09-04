#!/usr/bin/python3
"""
a class Product that inherits from BaseModel:
"""
import models
from models.base_model import BaseModel


class Product(BaseModel):
    """
    Product class
    """

    name = ''
    unit_price = 0
    stock = 0