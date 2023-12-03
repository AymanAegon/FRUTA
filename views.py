from flask import Blueprint, render_template, request, redirect
from models import storage
from models.client import Client
from models.product import Product
from models.order import Order
from flask_login import login_user, login_required, logout_user, current_user
from models import storage

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def products():
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
    return render_template("products.html", statsinfo=statsinfo, products_active=True, products=products)

@views.route('/clients')
@login_required
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
@login_required
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
        obj["id"] = order.id
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
@login_required
def blank():
    return render_template("blank.html")

@views.route('/create_product', methods=['GET', 'POST'])
@login_required
def create_product():
    messages = []
    if request.method == 'GET':
        return render_template("create_product.html", messages=messages, products_active=True)
    else:
        product_name = request.form['product_name']
        product_price = request.form['product_price']
        product_unit = request.form['product_unit']
        product_stock = request.form['product_stock']
        if product_name is None or product_name == "":
            messages.append(('error', "You must put a name!"))
            return render_template("create_product.html", messages=messages, products_active=True)
        if product_price is None or product_price == "":
            messages.append(('error', "You must set the Price!"))
            return render_template("create_product.html", messages=messages, products_active=True)
        try:
            product_price = float(product_price)
        except ValueError:
            messages.append(('error', "The Price must be a number!"))
            return render_template("create_product.html", messages=messages, products_active=True)
        if product_price < 0:
            messages.append(('error', "The Price must be positive!"))
            return render_template("create_product.html", messages=messages, products_active=True)
        try:
            product_stock = float(product_stock)
        except ValueError:
            messages.append(('error', "The Quantity must be a number!"))
            return render_template("create_product.html", messages=messages, products_active=True)
        if product_stock < 0:
            messages.append(('error', "The Quantity must be positive!"))
            return render_template("create_product.html", messages=messages, products_active=True)

        new_product = Product()
        new_product.name = product_name
        new_product.unit_price = product_price
        new_product.unit_name = product_unit
        new_product.stock = product_stock
        new_product.save()
        return redirect('/')

@views.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    clients = storage.all(Client).values()
    products = storage.all(Product).values()
    messages = []
    if request.method == 'GET':
        return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
    else:
        client_id = request.form['client_info']
        product = request.form['product']
        quantity = request.form['quantity']
        if client_id is None or client_id == "":
            messages.append(('error', "You must set a client!"))
            return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
        if product is None or product == "":
            messages.append(('error', "You must set a product!"))
            return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
        if quantity is None or quantity == "":
            messages.append(('error', "You must set the Quantity!"))
            return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
        try:
            quantity = float(quantity)
        except ValueError:
            messages.append(('error', "The Quantity must be a number!"))
            return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)

        quantity = float(quantity)
        product_obj = storage.get(Product, product)
        if quantity > float(product_obj.stock):
            messages.append(('error', "There is not enough stock!"))
            return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
        price = float(quantity) * float(product_obj.unit_price)
        new_order = Order()
        new_order.client_id = client_id
        new_order.product_id = product
        new_order.quantity = quantity
        new_order.total_price = price
        new_order.save()
        product_obj.stock = float(product_obj.stock) - float(quantity)
        product_obj.save()
        return redirect('/orders')

@views.route('/create_client', methods=['GET', 'POST'])
@login_required
def create_client():
    messages = []
    if request.method == 'GET':
        return render_template("create_client.html", messages=messages, clients_active=True)
    else:
        name = request.form['client_name']
        tel_number = request.form['phone_number']
        if name is None or name == "":
            messages.append(('error', "You must put a name!"))
            return render_template("create_client.html", messages=messages, clients_active=True)
        if tel_number is None or tel_number == "":
            messages.append(('error', "You must put the Phone number!"))
            return render_template("create_client.html", messages=messages, clients_active=True)
        clients = storage.all(Client).values()
        for client in clients:
            if tel_number == client.tel_number:
                messages.append(('error', "Phone number already exist!"))
                return render_template("create_client.html", messages=messages, clients_active=True)
        new_client = Client()
        new_client.name = name
        new_client.tel_number = tel_number
        new_client.user_id = current_user.id
        new_client.save()
        return redirect('/clients')

@views.route('/product_info/<product_id>')
@login_required
def product_info(product_id):
    product = storage.get(Product, product_id)
    if product is None:
        return render_template('404.html'), 404
    return render_template("product_info.html", home_active=True, product=product)

@views.route('/client_info/<client_id>')
@login_required
def client_info(client_id):
    client = storage.get(Client, client_id)
    if client is None:
        return render_template('404.html'), 404
    return render_template("client_info.html", clients_active=True, client=client)

@views.route('/order_info/<order_id>')
@login_required
def order_info(order_id):
    order = storage.get(Order, order_id)
    if order is None:
        return render_template('404.html'), 404
    return render_template("order_info.html", orders_active=True, order=order)
    