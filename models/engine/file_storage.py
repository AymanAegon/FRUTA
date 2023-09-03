#!/usr/bin/python3
""" FileStorage class."""
import json
from models.base_model import BaseModel
# from models.user import Client
# from models.city import Order
# from models.place import Product
# from models.state import Box



class FileStorage:
    """ Serialize instances to a JSON file and viseversa."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Returns the __objects dictionary."""
        return self.__objects

    def new(self, obj):
        """ Sets in __Objects the obj with key<obj class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """ Serealizes __objects to JSON file (path: __file_path)."""
        obj_dict = {}
        for key, value in self.__objects.items():
            obj_dict[key] = value.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """ Deserializes the JSON file  (only if the JSON file exists)"""
        try:
            with open(self.__file_path, 'r') as file:
                obj_dict = json.load(file)
                for key in obj_dict.items():
                    class_name = key[1]["__class__"]
                    del key[1]["__class__"]
                    self.new(eval(class_name)(**key[1]))
        except FileNotFoundError:
            return