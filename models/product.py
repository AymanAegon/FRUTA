#!/usr/bin/python3
"""
a class Product that inherits from BaseModel:
"""
from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.base_model import BaseModel, Base
import models
from models.order import Order



class Product(BaseModel, Base):
    """
    Product class
    """
    if models.StorageType == 'db':
        __tablename__ = "products"
        name = Column(String(128), nullable=False)
        unit_price = Column(Float, nullable=False)
        unit_name = Column(String(128), nullable=True, default="unit")
        primary_stock = Column(Float, nullable=False, default=0)
        stock = Column(String(128), nullable=False, default=0)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

        # Add ForeignKey constraint to the orders relationship
        orders = relationship("Order", cascade="all,delete", backref="product")
        fees = relationship("Fee", backref="products")
       
    else:
        name = ''
        unit_price = 0
        unit_name = "unit"
        stock = 0
        user_id = ''


    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.StorageType != "db":
        @property
        def orders(self):
            """getter for list of order instances related to the product"""
            order_list = []
            all_orders = models.storage.all(Order)
            for order in all_orders.values():
                if order.product_id == self.id:
                    order_list.append(order)
            return order_list