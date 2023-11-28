from models import storage
from models.base_model import BaseModel
from models.product import Product
from models.client import Client

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

# print("-- Create a new Product --")
# my_product = Product()
# my_product.name = "Banana"
# my_product.unit_price = 10.00
# my_product.stock = 100
# my_product.save()
# print(my_product)

# print("-- Create a new Client --")
# new_client = Client()
# new_client.name = "Ayman"
# new_client.tel_number = "0123456789"
# new_client.save()
# print(new_client)