#!/usr/bin/python3
"""
a class Client that inherits from BaseModel:
"""
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.base_model import BaseModel, Base
import models
from models.order import Order




class Client(BaseModel, Base):
    """
    Client class
    """
    if models.StorageType == 'db':
        __tablename__ = "clients"
        name = Column(String(128), nullable=False)
        tel_number = Column(String(60), nullable=True)

        # Add ForeignKey constraint to the orders relationship
        orders = relationship("Order", cascade="all,delete", backref="client")

    else:
        name = ''
        tel_number = ''


    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.StorageType != "db":
        @property
        def orders(self):
            """getter for list of order instances related to the client"""
            order_list = []
            all_orders = models.storage.all(Order)
            for order in all_orders.values():
                if order.client_id == self.id:
                    order_list.append(order)
            return order_list

