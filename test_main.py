from models import storage
from models.base_model import BaseModel
from models.product import Product

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new Product --")
my_product = Product()
my_product.name = "Banana"
my_product.unit_price = 10.00
my_product.stock = 100
my_product.save()
print(my_product)

print("-- Create a new Product 2 --")
my_product2 = Product()
my_product2.name = "TV"
my_product2.unit_price = 3000.50
my_product.stock = 20
my_product2.save()
print(my_product2)