from flask import Blueprint, render_template, request, redirect
from models import storage
from models.client import Client
from models.product import Product
from models.order import Order

views = Blueprint('views', __name__)

@views.route('/')
def home():
    orders = storage.all(Order).values()
    revenue = 0
    for order in orders:
        revenue += order.total_price
    statsinfo = [
        len(storage.all(Product).values()),
        len(orders),
        revenue,
        len(storage.all(Client).values())
    ]
    products = storage.all(Product).values()
    return render_template("index.html", statsinfo=statsinfo, home_active=True, products=products)

@views.route('/orders')
def orders():
    orders = storage.all(Order).values()
    revenue = 0
    for order in orders:
        revenue += order.total_price
    statsinfo = [
        len(storage.all(Product).values()),
        len(orders),
        revenue,
        len(storage.all(Client).values())
    ]
    return render_template("orders.html", statsinfo=statsinfo, orders_active=True)

@views.route('/clients')
def clients():
    orders = storage.all(Order).values()
    revenue = 0
    for order in orders:
        revenue += order.total_price
    statsinfo = [
        len(storage.all(Product).values()),
        len(orders),
        revenue,
        len(storage.all(Client).values())
    ]
    clients = storage.all(Client).values()
    return render_template("clients.html", statsinfo=statsinfo, clients_active=True, clients=clients)

@views.route('/blank')
def blank():
    return render_template("blank.html")

@views.route('/create_product', methods=['GET', 'POST'])
def create_product():
    messages = []
    if request.method == 'GET':
        return render_template("create_product.html", messages=messages, create_client=True)
    else:
        product_name = request.form['product_name']
        product_price = request.form['product_price']
        product_unit = request.form['product_unit']
        product_stock = request.form['product_stock']
        if product_name is None or product_name == "":
            messages.append(('error', "You must put a name!"))
            return render_template("create_product.html", messages=messages, create_client=True)
        if product_price is None or product_price == "":
            messages.append(('error', "You must set the Price!"))
            return render_template("create_product.html", messages=messages, create_client=True)

        new_product = Product()
        new_product.name = product_name
        new_product.unit_price = product_price
        new_product.unit_name = product_unit
        new_product.stock = product_stock
        new_product.save()
        return redirect('/')

@views.route('/create_client', methods=['GET', 'POST'])
def create_client():
    messages = []
    if request.method == 'GET':
        return render_template("create_client.html", messages=messages, create_client=True)
    else:
        name = request.form['client_name']
        tel_number = request.form['phone_number']
        if name is None or name == "":
            messages.append(('error', "You must put a name!"))
            return render_template("create_client.html", messages=messages, create_client=True)
        if tel_number is None or tel_number == "":
            messages.append(('error', "You must put the Phone number!"))
            return render_template("create_client.html", messages=messages, create_client=True)
        clients = storage.all(Client).values()
        for client in clients:
            if tel_number == client.tel_number:
                messages.append(('error', "Phone number already exist!"))
                return render_template("create_client.html", messages=messages, create_client=True)
        new_client = Client()
        new_client.name = name
        new_client.tel_number = tel_number
        new_client.save()
        return redirect('/clients')
    