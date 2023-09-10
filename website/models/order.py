#!/usr/bin/python3
"""
a class Order that inherits from BaseModel:
"""
import models
from models.base_model import BaseModel


class Order(BaseModel):
    """
    Order class
    """

    client_id = ''
    product_id = ''
    quantity = 0
    total_price = 0
    number_box = 0