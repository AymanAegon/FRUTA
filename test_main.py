from models import storage
from models.base_model import BaseModel
from models.product import Product
from models.client import Client
from models.user import User

all_objs = storage.all(User)
print("-- Reloaded user objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

# print("-- Create a new user --")
# my_user = User()
# my_user.name = 'oussama'
# my_user.email = 'oussama@gmail.com'
# my_user.password = 'oussama_pwd'
# my_user.save()
# print(my_user)

# print("-- Create a new Client --")
# new_client = Client()
# new_client.name = "Ayman"
# new_client.tel_number = "0123456789"
# new_client.save()
# print(new_client)