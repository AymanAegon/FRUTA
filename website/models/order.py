#!/usr/bin/python3
"""
a class Order that inherits from BaseModel:
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models.client import Client
from models.product import Product
from models.boxes_out import Box_out
from models.boxes_in import Box_in
from os import getenv



storage_type = getenv("FRUTA_TYPE_STORAGE")






class Order(BaseModel, Base):
    """
    Order class
    """
    __tablename__ = "orders"
    if storage_type == "db":

        client_id = Column(String(60), ForeignKey("clients.id"), nullable=False)
        product_id =Column(String(60), ForeignKey("products.id"), nullable=False)
        quantity = Column(Float,nullable=False)
        total_price = Column(Float,nullable=False)
        box_out = Column(Integer,primary_keys=True,nullable=False)
        box_in = Column(Integer,primary_keys=True,nullable=False)

        boxes_out = relationship("Box_out", backref="order")
        boxes_in = relationship("Box_in", backref="order")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.update_client_box_out()

        def update_client_box_out(self):
            client = self.client
            if client:
                client.box_out += self.box_out


    else:
        client_id = ''
        product_id = ''
        quantity = 0
        total_price = 0
        box_out = 0

