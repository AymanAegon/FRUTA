#!/usr/bin/python3
"""
a class Product that inherits from BaseModel:
"""
from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.base_model import BaseModel, Base
import models



class Fee(BaseModel, Base):
    """
    Fee class
    """
    if models.StorageType == 'db':
        __tablename__ = "fees"
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        product_id = Column(String(60), ForeignKey("products.id"), nullable=False, unique= True)
        warehouse_loader = Column(Float, default=70, nullable=False)
        cutting= Column(Float, default=300, nullable=False)
        gaz = Column(Float, default=0, nullable=False)
        to_market = Column(Float, default=150, nullable=False)
        boxes_fee = Column(Float, default=80, nullable=False)
        market_loader = Column(Float, default=70, nullable=False)
        weight_lost = Column(Float, default=161, nullable=False)
        fuel = Column(Float, default=0, nullable=False)
        others = Column(Float, default=20, nullable=False)
        total_cost= Column(Float, default=0, nullable=False)
        price_per_unit = Column(Float, default=0, nullable=False)
        

        # Add ForeignKey constraint to the orders relationship
        
       
    else:
        product_id = ''
        to_warehouse = 70
        cutting = 300
        gaz = 0
        electricity = ''
        controle = 0
        to_market = 150
        boxes_fee = 80
        loader = 0
        weight_lost = 0
        others = 20
