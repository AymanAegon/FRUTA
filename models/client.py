#!/usr/bin/python3
"""
a class Client that inherits from BaseModel:
"""
import models
from models.base_model import BaseModel


class Client(BaseModel):
    """
    Client class
    """

    name = ''
    tel_number = ''
    box_left = 0