#!/usr/bin/python3
""" FileStorage class."""
import json
from models.base_model import BaseModel
from models.client import Client
from models.product import Product
from models.boxes_out import Box_out
from models.boxes_in import Box_in
from models.order import Order




classes = {"Client": Client, "BaseModel": BaseModel, "Order": Order,
           "Product": Product, "Box_ou": Box_out,"Box_in":Box_in}

class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Method to return the object based on the class and its ID"""
        if cls:
            for value in self.__objects.values():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    if id == value.id:
                        return value
        return None

    def count(self, cls=None):
        """Returns the number of objects
        in storage matching the given class."""
        if cls:
            all_objs_dict = self.all(cls)
            count = len(all_objs_dict)
        else:
            count = len(self.all())
        return count