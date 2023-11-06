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

        box_out = Column(Integer, nullable=False, default=0)
        box_left = Column(Integer, nullable=False, default=0)

        orders = relationship("Order", cascade="all,delete", backref="client")
        boxes_out = relationship("Box_out", back_populates="client")
        boxes_in = relationship("Box_in", back_populates="client")
    else:
        name = ''
        tel_number = ''
        box_out = 0
        box_left = 0

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def orders(self):
            """getter for list of city instances related to the state"""
            order_list = []
            all_orders = models.storage.all(Order)
            for order in all_orders.values():
                if order.client_id == self.id:
                    order_list.append(order)
            return order_list

