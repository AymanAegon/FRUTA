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

@views.route('/orders')
def orders():
    orders = storage.all(Order).values()
    revenue = 0
    results = []
    obj = {}
    for order in orders:
        revenue += order.total_price
        obj["client_name"] = storage.get(Client, order.client_id).name
        obj["client_tel"] = storage.get(Client, order.client_id).tel_number
        obj["product"] = storage.get(Product, order.product_id).name
        obj["quantity"] = order.quantity
        obj["total_price"] = order.total_price
        obj["created_at"] = order.created_at
        results.append(obj.copy())

    statsinfo = [
        len(storage.all(Product).values()),
        len(orders),
        revenue,
        len(storage.all(Client).values())
    ]
    return render_template("orders.html", statsinfo=statsinfo, orders_active=True, orders=results)

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

@views.route('/create_order', methods=['GET', 'POST'])
def create_order():
    messages = []
    if request.method == 'GET':
        clients = storage.all(Client).values()
        products = storage.all(Product).values()
        return render_template("create_order.html", messages=messages, products=products, clients=clients)
    else:
        client_id = request.form['client_info']
        product = request.form['product']
        quantity = request.form['quantity']
        if client_id is None or client_id == "":
            messages.append(('error', "You must set a client!"))
            return render_template("create_order.html", messages=messages)
        if product is None or product == "":
            messages.append(('error', "You must set a product!"))
            return render_template("create_order.html", messages=messages)
        if quantity is None or quantity == "":
            messages.append(('error', "You must set the Quantity!"))
            return render_template("create_order.html", messages=messages)
        try:
            quantity = float(quantity)
        except ValueError:
            messages.append(('error', "The Quantity must be a number!"))
            return render_template("create_order.html", messages=messages)
        
        price = float(quantity) * storage.get(Product, product).unit_price
        new_order = Order()
        new_order.client_id = client_id
        new_order.product_id = product
        new_order.quantity = quantity
        new_order.total_price = price
        new_order.save()
        return redirect('/orders')

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
    