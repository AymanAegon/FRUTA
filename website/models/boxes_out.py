#!/usr/bin/python3
"""
a class Box that inherits from BaseModel:
"""
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from os import getenv
from models.base_model import BaseModel, Base

storage_type = getenv("FRUTA_TYPE_STORAGE")


class Box_out(BaseModel, Base):
    """
    Box class
    """
    __tablename__ = "boxes_out"
    if storage_type == 'db':

        quantity = Column(Integer, ForeignKey('orders.boxes_out') ,default=1) 
        order_id = Column(Integer, ForeignKey('orders.id'))
        client_id = Column(Integer, ForeignKey('clients.id'))

        client = relationship("Client", back_populates="boxes_out")
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.update_client_box_out()

        def update_client_box_out(self):
            client = self.client
            if client:
                client.box_out += self.quantity

    else:
        quantity = 0
        order_id = 0
        client_id = 0



