from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import storage
from models.client import Client
from models.product import Product
from models.order import Order
from models.user import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import storage

views = Blueprint('views', __name__)

# the route for the home page
@views.route('/home')
def landing_page():
    return render_template("index.html")

# the route for the products page
@views.route('/')
@login_required
def products():
    # stats data to display start
    revenue = 0
    # geting the user orders
    orders = current_user.orders
    for order in orders:
        # calculating the total revenue
        revenue += order.total_price
    # geting the user products
    products = current_user.products
    # geting the user clients
    clients = current_user.clients
    # creating the statinfo data list to display in the dashboard
    statsinfo = [len(products), len(orders), revenue, len(clients)]
    # statinfo data end
    return render_template("products.html", statsinfo=statsinfo, products_active=True, products=products)

# the route for the clients page
@views.route('/clients')
@login_required
def clients():
    # stats data start
    revenue = 0
    # geting the user orders
    orders = current_user.orders
    for order in orders:
        # calculating the total revenue
        revenue += order.total_price
    # geting the user products
    products = current_user.products
    # geting the user clients
    clients = current_user.clients
    # creating the statinfo data list to display in the dashboard
    statsinfo = [len(products), len(orders), revenue, len(clients)]
    # statinfo data end
    return render_template("clients.html", statsinfo=statsinfo, clients_active=True, clients=clients)

# the route for the orders page
@views.route('/orders')
@login_required
def orders():
    # stats data start
    revenue = 0
    # geting the user orders
    orders = current_user.orders
    for order in orders:
        # calculating the total revenue
        revenue += order.total_price
    # geting the user products
    products = current_user.products
    # geting the user clients
    clients = current_user.clients
    # creating the statinfo data list to display in the dashboard
    statsinfo = [len(products), len(orders), revenue, len(clients)]
    # stats data end
    ordersList = []
    obj = {}
    for order in orders:
        obj["client_name"] = storage.get(Client, order.client_id).name
        obj["client_tel"] = storage.get(Client, order.client_id).tel_number
        obj["product"] = storage.get(Product, order.product_id).name
        obj["id"] = order.id
        obj["quantity"] = order.quantity
        obj["total_price"] = order.total_price
        obj["created_at"] = order.created_at
        ordersList.append(obj.copy()) # copy to prevent overwriting the object
    return render_template("orders.html", statsinfo=statsinfo, orders_active=True, orders=ordersList)

# the route for the blank page
@views.route('/blank')
@login_required
def blank():
    return render_template("blank.html")

# the route for creating products
@views.route('/create_product', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'GET':
        # if GET requesting, render the page with the form to create a product
        return render_template("create_product.html", products_active=True)
    else:
        # if POST requesting, get the fields, check them and create the new product
        product_name = request.form['product_name']
        product_price = request.form['product_price']
        product_unit = request.form['product_unit']
        product_stock = request.form['product_stock']
        # running checks
        if product_name is None or product_name == "":
            flash('You must put a Name!', category="error")
            return render_template("create_product.html", products_active=True)
        if product_price is None or product_price == "":
            flash('You must set a Price!', category="error")
            return render_template("create_product.html", products_active=True)
        if product_unit is None or product_unit == "":
            flash('You must put a Unit!', category="error")
            return render_template("create_product.html", products_active=True)
        if product_stock is None or product_stock == "":
            flash('You must set the Quantity!', category="error")
            return render_template("create_product.html", products_active=True)
        try:
            product_price = float(product_price)
        except ValueError:
            flash('he Price must be a number!', category="error")
            return render_template("create_product.html", products_active=True)
        if product_price < 0:
            flash('The Price must be positive!', category="error")
            return render_template("create_product.html", products_active=True)
        try:
            product_stock = float(product_stock)
        except ValueError:
            flash('The Quantity must be a number!', category="error")
            return render_template("create_product.html", products_active=True)
        if product_stock < 0:
            flash('The Quantity must be positive!', category="error")
            return render_template("create_product.html", products_active=True)

        # creating the new product and saving it to the datadase
        new_product = Product()
        new_product.name = product_name
        new_product.unit_price = product_price
        new_product.unit_name = product_unit
        new_product.stock = product_stock
        new_product.user_id = current_user.id
        new_product.save()
        return redirect('/')

# the route for creating new orders
@views.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    # geting the user clients
    clients = current_user.clients
    arr = storage.all(Product).values()
    # geting the user products
    products = current_user.products
    messages = []
    if request.method == 'GET':
        # if GET requesting, render the page with the form of creating a new order
        return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
    else:
        # if POST requesting, get the fields, check them and create the new order
        client_id = request.form['client_info']
        product = request.form['product']
        quantity = request.form['quantity']
        # running checks
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

        # creating the new order and saving it to the datadase
        price = float(quantity) * float(product_obj.unit_price)
        new_order = Order()
        new_order.client_id = client_id
        new_order.product_id = product
        new_order.quantity = quantity
        new_order.total_price = price
        new_order.user_id = current_user.id
        new_order.save()
        # reducing the products available stock
        product_obj.stock = float(product_obj.stock) - float(quantity)
        product_obj.save()
        return redirect('/orders')

# the route for creating new clients
@views.route('/create_client', methods=['GET', 'POST'])
@login_required
def create_client():
    messages = []
    if request.method == 'GET':
        # if GET requesting, render the page with the form of creating a new client
        return render_template("create_client.html", messages=messages, clients_active=True)
    else:
        # if POST requesting, get the fields, check them and create the new client
        name = request.form['client_name']
        tel_number = request.form['phone_number']
        # running checks
        if name is None or name == "":
            messages.append(('error', "You must put a name!"))
            return render_template("create_client.html", messages=messages, clients_active=True)
        if tel_number is None or tel_number == "":
            messages.append(('error', "You must put the Phone number!"))
            return render_template("create_client.html", messages=messages, clients_active=True)
        clients = current_user.clients
        for client in clients:
            if tel_number == client.tel_number:
                messages.append(('error', "Phone number already exist!"))
                return render_template("create_client.html", messages=messages, clients_active=True)

        # creating the new client and saving it to the datadase
        new_client = Client()
        new_client.name = name
        new_client.tel_number = tel_number
        new_client.user_id = current_user.id
        new_client.save()
        return redirect('/clients')

# the route for the client info page
@views.route('/client/<client_id>')
@login_required
def client_info(client_id):
    # getting the client with the id passed in the request
    client = storage.get(Client, client_id)
    if client is None:  # checking if the client with id=client_id exists
        return render_template('404.html'), 404
    if current_user.id != client.user_id:  # checking if user is the owner of the client
        flash('An error has occurred!', category="error")
        return redirect('/clients')
    
    # getting all the orders made by the client and calculating total spending
    orders = client.orders
    spendings = 0
    for order in orders:
        spendings += order.total_price
    return render_template("client_info.html", clients_active=True, client=client, spendings=spendings)

# the route for listing all orders made by a client
@views.route('/client/<client_id>/orders')
@login_required
def client_orders(client_id):
    # getting the client with the id passed in the request
    client = storage.get(Client, client_id)
    if client is None:  # checking if the client with id=client_id exists
        return render_template('404.html'), 404
    if current_user.id != client.user_id:  # checking if user is the owner of the client
        flash('An error has occurred!', category="error")
        return redirect('/')
    
    # Loading all the orders in the wanted format
    results = []
    obj = {}
    for order in client.orders:
        obj["client_name"] = client.name
        obj["client_tel"] = storage.get(Client, order.client_id).tel_number
        obj["product"] = storage.get(Product, order.product_id).name
        obj["id"] = order.id
        obj["quantity"] = order.quantity
        obj["total_price"] = order.total_price
        obj["created_at"] = order.created_at
        results.append(obj.copy())
    return render_template("specific_orders.html", clients_active=True, orders=results, obj=client)

# the route for deleting a client
@views.route('/delete_client/<client_id>')
@login_required
def delete_client(client_id):
    # getting the client with the id passed in the request
    client = storage.get(Client, client_id)
    if client is None:  # checking if the client with id=client_id exists
        return render_template('404.html'), 404
    if current_user.id != client.user_id:  # checking if user is the owner of the client
        flash('An error has occurred!', category="error")
        return redirect('/')
    
    # deleting the client using the BaseModel.delete() method
    client.delete()
    storage.save()
    # show the success message
    flash('Client has been deleted!', category="success")
    return redirect('/clients')

# the route for editing a client
@views.route('/edit_client/<client_id>', methods=['GET', 'POST'])
@login_required
def edit_client(client_id):
    # getting the client with the id passed in the request
    client = storage.get(Client, client_id)
    if client is None:  # checking if the client with id=client_id exists
        return render_template('404.html'), 404
    if current_user.id != client.user_id:  # checking if user is the owner of the client
        flash('An error has occurred!', category="error")
        return redirect('/')

    if request.method == 'POST':
        # if POST requesting, get the fields, check them and edit the client
        name = request.form['client_name']
        tel_number = request.form['phone_number']
        # running checks
        if name is None or name == "":
            flash('You must put a name!', category="error")
            return render_template("edit_client.html", clients_active=True, client=client)
        if tel_number is None or tel_number == "":
            flash('You must put the Phone number!', category="error")
            return render_template("edit_client.html", clients_active=True, client=client)
        clients = current_user.clients
        for obj in clients:
            if client.id != obj.id and tel_number == obj.tel_number:
                flash('Phone number already exist!', category="error")
                return render_template("edit_client.html", clients_active=True, client=client)
        # editing the client and save
        client.name = name
        client.tel_number = tel_number
        client.save()
        return redirect(url_for('views.client_info', client_id=client_id))
    # if GET requesting, render the page with the form of editing the client
    return render_template("edit_client.html", clients_active=True, client=client)

# the route for the product info page
@views.route('/product_info/<product_id>')
@login_required
def product_info(product_id):
    # getting the product with the id passed in the request
    product = storage.get(Product, product_id)
    if product is None:  # checking if the product with id=product_id exists
        return render_template('404.html'), 404
    if current_user.id != product.user_id:  # checking if user is the owner of the product
        flash('An error has occurred!', category="error")

    # getting all the orders of the product and calculating the total revenue
    revenue = 0
    for order in product.orders:
        revenue += order.total_price
    return render_template("product_info.html", products_active=True, product=product, revenue=revenue)

# the route for listing all orders of the product
@views.route('/product/<product_id>/orders')
@login_required
def product_orders(product_id):
    # getting the product with the id passed in the request
    product = storage.get(Product, product_id)
    if product is None:  # checking if the product with id=product_id exists
        return render_template('404.html'), 404
    if current_user.id != product.user_id:  # checking if user is the owner of the product
        flash('An error has occurred!', category="error")
        return redirect('/')
    
    # Loading all the orders in the wanted format
    results = []
    obj = {}
    for order in product.orders:
        obj["client_name"] = storage.get(Client, order.client_id).name
        obj["client_tel"] = storage.get(Client, order.client_id).tel_number
        obj["product"] = product.name
        obj["id"] = order.id
        obj["quantity"] = order.quantity
        obj["total_price"] = order.total_price
        obj["created_at"] = order.created_at
        results.append(obj.copy())
    return render_template("specific_orders.html", products_active=True, orders=results, obj=product)

# the route for editing a product
@views.route('/edit_product/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    # getting the product with the id passed in the request
    product = storage.get(Product, product_id)
    if product is None:  # checking if the product with id=product_id exists
        return render_template('404.html'), 404
    if current_user.id != product.user_id:  # checking if user is the owner of the product
        flash('An error has occurred!', category="error")

    if request.method == 'POST':
        # if POST requesting, get the fields, check them and edit the product
        product_name = request.form['product_name']
        product_price = request.form['product_price']
        product_unit = request.form['product_unit']
        product_stock = request.form['product_stock']
        # running checks
        if product_name is None or product_name == "":
            flash('You must put a Name!', category="error")
            return render_template("edit_product.html", products_active=True, product=product)
        if product_price is None or product_price == "":
            flash('You must set a Price!', category="error")
            return render_template("edit_product.html", products_active=True, product=product)
        if product_unit is None or product_unit == "":
            flash('You must put a Unit!', category="error")
            return render_template("edit_product.html", products_active=True, product=product)
        if product_stock is None or product_stock == "":
            flash('You must set the Quantity!', category="error")
            return render_template("edit_product.html", products_active=True, product=product)
        try:
            product_price = float(product_price)
        except ValueError:
            flash('The Price must be a number!', category="error")
            return render_template("edit_product.html", products_active=True, product=product)
        if product_price < 0:
            flash('The Price must be positive!', category="error")
            return render_template("edit_product.html", products_active=True, product=product)
        try:
            product_stock = float(product_stock)
        except ValueError:
            flash('The Quantity must be a number!', category="error")
            return render_template("edit_product.html", products_active=True, product=product)
        if product_stock < 0:
            flash('The Quantity must be positive!', category="error")
            return render_template("edit_product.html", products_active=True, product=product)
        # editing the product and save
        product.name = product_name
        product.unit_price = product_price
        product.unit_name = product_unit
        product.stock = product_stock
        product.save()
        return redirect(url_for('views.product_info', product_id=product_id))
    # if GET requesting, render the page with the form of editing the product
    return render_template("edit_product.html", products_active=True, product=product)

# the route for deleting a product
@views.route('/delete_product/<product_id>')
@login_required
def delete_product(product_id):
    # getting the product with the id passed in the request
    product = storage.get(Product, product_id)
    if product is None:  # checking if the product with id=product_id exists
        return render_template('404.html'), 404
    if current_user.id != product.user_id:  # checking if user is the owner of the product
        flash('An error has occurred!', category="error")
        return redirect('/')
    
    # deleting the product using the BaseModel.delete() method
    product.delete()
    storage.save()
    # show the success message
    flash('Product has been deleted!', category="success")
    return redirect('/')

# the route for the order info page
@views.route('/order_info/<order_id>')
@login_required
def order_info(order_id):
    # getting the order with the id passed in the request
    order = storage.get(Order, order_id)
    if order is None:  # checking if the order with id=order_id exists
        return render_template('404.html'), 404
    if current_user.id != order.user_id:  # checking if user is the owner of the order
        flash('An error has occurred!', category="error")
    # this is rending a blank page for now
    return render_template("order_info.html", orders_active=True, order=order)

# the route for the profile page
@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # if POST requesting, get the name field and edit the user's name and save
        name = request.form['name']
        if name is None or name == "": # checking if the name is not empty
            flash('Name can not be empty!', category="error")
            return render_template("change_password.html", user=current_user)
        # editing the name and save
        current_user.name = name
        current_user.save()
        flash('Your name has been changed!', category="success")
    # if GET requesting, render the page with user info
    return render_template("profile.html", user=current_user)

# the route for changing user's password
@views.route('/profile/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
    # if POST requesting, get the fields and edit the user's password
        old_pwd = request.form['old_pwd']
        new_pwd1 = request.form['new_pwd1']
        new_pwd2 = request.form['new_pwd2']
        # running checks
        if old_pwd is None or old_pwd == "":
            flash('Field can not be empty!', category="error")
        elif new_pwd1 is None or new_pwd1 == "":
            flash('Field can not be empty!', category="error")
        elif new_pwd2 is None or new_pwd2 == "":
            flash('Field can not be empty!', category="error")
        elif check_password_hash(current_user.password, old_pwd) is False:
            flash('Incorrect password, Try again!', category="error")
        elif len(new_pwd1) < 8:
            flash('Password must be greater than 8 characters!', category="error")
        elif new_pwd1 != new_pwd2:
            flash('Passwords don\'t match', category="error")
        else:
            # when evreything checks, change the passowrd and save
            current_user.password = generate_password_hash(new_pwd1, method="scrypt")
            current_user.save()
            # show the success message
            flash('Password changed successfully!', category="success")
            return redirect(url_for('views.profile'))
    # if GET requesting, render the page with the form of changing the password
    return render_template("change_password.html", user=current_user)
    
