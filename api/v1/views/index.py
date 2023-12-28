#!/usr/bin/python3
"""define routes of blueprint
"""

from api.v1.views import app_views
from models import storage
from models.client import Client
from models.order import Order
from models.product import Product
from models.boxe_in import Boxe_in



@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    return {
        "status": "OK",
    }


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def stats():
    products = storage.count(Product)
    clients = storage.count(Client)
    orders = storage.count(Order)
    boxes = storage.count(Boxe)

    return {
        "products": products,
        "clients": clients,
        "orders": orders,
        "boxes": boxes,
        "states": states,
        "users": users,
    }