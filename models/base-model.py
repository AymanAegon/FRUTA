#!/usr/bin/python3
"""
base_model class
"""

import models
from datetime import datetime
import uuid


class BaseModel():
    """
    BaseModel class implementation
    Methods:
        __init__(self, *args, **kwargs)
        __str__(self)
        __save(self)
        __repr__(self)
        to_dict(self)
    """

    def __init__(self, *arg, **kwargs):
        """
        initializes an instance
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            t = '%Y-%m-%dT%H:%M:%S.%f'
            for key, value in kwargs.items():
                if key == "created_at":
                    self.created_at = datetime.strptime(value, t)
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(value, t)
                elif key != "__class__":
                    setattr(self, key, value)
        else:
            models.storage.new(self)

    def __str__(self) -> str:
        """
        returns info about an instance
        """
        a = self.__class__.__name__
        b = self.id
        c = self.__dict__
        return "[{}] ({}) <{}>".format(a, b, c)

    def save(self):
        """
        updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary
        containing all keys/values of __dict__ of the required instance
        """
        dic = {}
        dic["__class__"] = self.__class__.__name__
        for key, value in self.__dict__.items():
            if isinstance(value, (datetime, )):
                dic[key] = value.isoformat()
            else:
                dic[key] = value
        return dic