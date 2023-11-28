#!/usr/bin/python3
"""
a class Box that inherits from BaseModel:
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.base_model import BaseModel, Base

storage_type = getenv("FRUTA_TYPE_STORAGE")


class Box_in(BaseModel, Base):
    """
    Box class
    """
    __tablename__ = "boxes_in"
    if storage_type == 'db':
        return_id = Column(Integer, default=1,autoincrement=True)
        quantity = Column(Integer, default=1) 
        client_id = Column(Integer, ForeignKey('clients.id'))
    
        client = relationship("Client", back_populates="boxes_in")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.update_client_box_left()

        def update_client_box_left(self):
            client = self.client
            if client:
                client.box_left += self.quantity

    else:
        quantity = 0
        client_id = 0
        return_id = 0
