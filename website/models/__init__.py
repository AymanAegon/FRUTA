#!/usr/bin/python3
"""__init__ intilization"""

from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()