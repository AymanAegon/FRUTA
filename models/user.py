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
from models.product import Product
from models.client import Client
from flask_login import UserMixin

if models.StorageType == 'db':
    User_mixin = UserMixin
else:
    User_mixin = object

class User(BaseModel, Base):
    """
    User class
    """
    if models.StorageType == 'db':
        __tablename__ = "users"
        name = Column(String(128), nullable=False)
        email = Column(String(128), unique=True, nullable=False)
        password = Column(String(128), nullable=False)

        # Add ForeignKey constraint to the orders relationship
        products = relationship("Product", cascade="all,delete", backref="user")
        clients = relationship("Client", cascade="all,delete", backref="user")
        orders = relationship("Order", cascade="all,delete", backref="user")

    else:
        name = ''
        email = ''
        password = ''

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.StorageType != "db":
        @property
        def products(self):
            """getter for list of product instances related to the user"""
            product_list = []
            all_products = models.storage.all(Product)
            for product in all_products.values():
                if product.user_id == self.id:
                    product_list.append(product)
            return product_list

    if models.StorageType != "db":
        @property
        def clients(self):
            """getter for list of client instances related to the user"""
            client_list = []
            all_clients = models.storage.all(Client)
            for client in all_clients.values():
                if client.user_id == self.id:
                    client_list.append(client)
            return client_list

    if models.StorageType != "db":
        @property
        def orders(self):
            """getter for list of order instances related to the user"""
            order_list = []
            all_orders = models.storage.all(Order)
            for order in all_orders.values():
                if order.user_id == self.id:
                    order_list.append(order)
            return order_list

    __hash__ = object.__hash__

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    def __eq__(self, other):
        """
        Checks the equality of two `UserMixin` objects using `get_id`.
        """
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        """
        Checks the inequality of two `UserMixin` objects using `get_id`.
        """
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal
