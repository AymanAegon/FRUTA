#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""

from models.engine.db_storage import DBStorage
from os import getenv

StorageType = getenv('HBNB_TYPE_STORAGE')
if StorageType == 'db':
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()