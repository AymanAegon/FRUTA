from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import storage
from models.client import Client
from models.product import Product
from models.order import Order
from models.user import User
from models.boxe_in import Boxe_in
from models.fee import Fee
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import desc,and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

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
    products = storage.session.query(Product).filter_by(user_id=current_user.id).order_by(desc(Product.created_at)).all()


    # geting the user clients
    clients = current_user.clients
    
    boxes_out = 0
    for client in clients:
        boxes_out += client.boxes_number 

   # geting the boxes out number
    boxes = current_user.boxes_in
    fees = current_user.fees

    # creating the statinfo data list to display in the dashboard

    statsinfo = [len(products), len(orders), revenue, len(clients),boxes_out]
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
    clients = storage.session.query(Client).filter_by(user_id=current_user.id).order_by((Client.name)).all()
    boxes_out = 0
    for client in clients:
        boxes_out += client.boxes_number 
   # geting the boxes out number
    boxes = current_user.boxes_in
    fees = current_user.fees

    # creating the statinfo data list to display in the dashboard

    statsinfo = [len(products), len(orders), revenue, len(clients),boxes_out]
    # statinfo data end
    return render_template("clients.html", statsinfo=statsinfo, clients_active=True, clients=clients)

# the route for the orders page
@views.route('/orders')
@login_required
def orders():
    # stats data start
    revenue = 0
    # geting the user orders
    orders = sorted(current_user.orders,key=lambda k: k.created_at,reverse=True)
    for order in orders:
        # calculating the total revenue
        revenue += order.total_price
    # geting the user products
    products = current_user.products
    # geting the user clients
    clients = current_user.clients
    boxes_out = 0
    for client in clients:
        boxes_out += client.boxes_number 
   # geting the boxes out number
    boxes = current_user.boxes_in
    fees = current_user.fees

    # creating the statinfo data list to display in the dashboard

    statsinfo = [len(products), len(orders), revenue, len(clients),boxes_out]
    # stats data end
    ordersList = []
    obj = {}
    for order in orders:
        obj["client_name"] = storage.get(Client, order.client_id).name
        obj["client_tel"] = storage.get(Client, order.client_id).tel_number
        obj["product"] = storage.get(Product, order.product_id).name
        obj["id"] = order.id
        obj["quantity"] = order.quantity
        obj["boxes_number"] = order.boxes_number
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
        new_product.primary_stock = product_stock
        new_product.user_id = current_user.id
        new_product.save()
        return redirect('/')

# the route for creating new orders
@views.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    # geting the user clients
    clients = storage.session.query(Client).filter_by(user_id=current_user.id).order_by((Client.name)).all()
    arr = storage.all(Product).values()
    # geting the user products
    products = storage.session.query(Product).filter(and_(Product.user_id==current_user.id, Product.stock>0)).order_by(desc(Product.created_at)).all()
    messages = []
    if request.method == 'GET':
        # if GET requesting, render the page with the form of creating a new order
        return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
    else:
        # if POST requesting, get the fields, check them and create the new order
        client_id = request.form['client_info']
        product = request.form['product']
        quantity = request.form['quantity']
        boxes_number = request.form['boxes_number']
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
        if boxes_number is None or boxes_number == "":
            messages.append(('error', "You must set the Number of Boxes!"))
            return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
        try:
            quantity = float(quantity)
        except ValueError:
            messages.append(('error', "The Quantity must be a number!"))
            return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
        try:
            boxes_number = int(boxes_number)
        except ValueError:
            messages.append(('error', "The boxes numebr must be a number!"))
            return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
        quantity = float(quantity)
        boxes_number = int(boxes_number)
        product_obj = storage.get(Product, product)
        if quantity > float(product_obj.stock):
            messages.append(('error', "There is not enough stock!"))
            return render_template("create_order.html", messages=messages, products=products, clients=clients, orders_active=True)
        client_obj = storage.get(Client, client_id)


        # creating the new order and saving it to the datadase
        price = float(quantity) * float(product_obj.unit_price)
        new_order = Order()
        new_order.client_id = client_id
        new_order.product_id = product
        new_order.quantity = quantity
        new_order.boxes_number = boxes_number
        new_order.total_price = price
        new_order.user_id = current_user.id
        new_order.save()
        # reducing the products available stock
        product_obj.stock = float(product_obj.stock) - float(quantity)
        product_obj.save()
        if client_obj.boxes_number is not None:
            client_obj.boxes_number = int(client_obj.boxes_number) + int(boxes_number)
        else:
    # Handle the case where client_obj.boxes_number is None, perhaps set it to the value of boxes_number
            client_obj.boxes_number = int(boxes_number)
        client_obj.save()
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
    
# the route for the boxes page
@views.route('/boxes_in')
@login_required
def boxes_in():
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
    boxes_out = 0
    for client in clients:
        boxes_out += client.boxes_number 
   # geting the boxes out number
    boxes = storage.session.query(Boxe_in).filter_by(user_id=current_user.id).order_by(desc(Boxe_in.created_at)).all()
    fees = current_user.fees

    # creating the statinfo data list to display in the dashboard

    statsinfo = [len(products), len(orders), revenue, len(clients),boxes_out]
    # statinfo data end
    boxesList = []
    obj = {}
    for boxe in boxes:
        obj["client_name"] = storage.get(Client, boxe.client_id).name
        obj["client_tel"] = storage.get(Client, boxe.client_id).tel_number
        obj["id"] = boxe.id
        obj["boxes_number"] = boxe.boxes_number
        obj["created_at"] = boxe.created_at
        boxesList.append(obj.copy()) # copy to prevent overwriting the object
    return render_template("boxes_in.html", statsinfo=statsinfo, boxes_active=True, boxes=boxesList)

# the route for returning the boxes
@views.route('/return_boxes', methods=['GET', 'POST'])
@login_required
def return_boxes():
    # geting the user clients
    clients = storage.session.query(Client).filter_by(user_id=current_user.id).order_by((Client.name)).all()
    arr = storage.all(Product).values()
    # geting the user products
    products = current_user.products
    messages = []
    if request.method == 'GET':
        # if GET requesting, render the page with the form of creating a new order
        return render_template("return_boxes.html", messages=messages, clients=clients)
    else:
        # if POST requesting, get the fields, check them and create the new order
        client_id = request.form['client_info']
        boxes_number = request.form['boxes_number']
        # running checks
        if client_id is None or client_id == "":
            messages.append(('error', "You must set a client!"))
            return render_template("return_boxes.html", messages=messages, clients=clients)
        if boxes_number is None or boxes_number == "":
            messages.append(('error', "You must set a number!"))
            return render_template("return_boxes.html", messages=messages, clients=clients)
        try:
            boxes_number = float(boxes_number)
        except ValueError:
            messages.append(('error', "The boxes_number must be a number!"))
            return render_template("return_boxes.html", messages=messages, clients=clients)
        boxes_number = int(boxes_number)
        client_obj = storage.get(Client, client_id)
        if boxes_number > float(client_obj.boxes_number):
            messages.append(('error', "There client did not took this number"))
            return render_template("return_boxes.html", messages=messages, products=products, clients=clients, boxes_active=True)


        # returning a new boxes and saving it to the datadase
        backup = Boxe_in()
        backup.client_id = client_id
        backup.boxes_number = boxes_number

        backup.user_id = current_user.id
        backup.save()
        # reducing the boxes_number displayed for the client
        client_obj.boxes_number = int(client_obj.boxes_number) - int(boxes_number)
        client_obj.save()
        return redirect('/boxes_in')
    
# the route for adding fees
@views.route('/add_fee', methods=['GET', 'POST'])
@login_required
def add_fee():

    existing_product_ids = set(fee.product_id for fee in current_user.fees)
    sorted_products = storage.session.query(Product).filter_by(user_id=current_user.id).order_by(desc(Product.created_at)).all()
    products = [product for product in sorted_products if product.id not in existing_product_ids]

    if request.method == 'GET':
        # if GET requesting, render the page with the form to create a product
        return render_template("add_fee.html", fees_active=True,products = products)
    else:
        # if POST requesting, get the fields, check them and create the new product
        product_id = request.form['product_info']
        warehouse_loader = float(request.form['warehouse_loader'])
        cutting = float(request.form['cutting'])
        to_market = float(request.form['to_market'])
        gaz = float(request.form['gaz'])
        boxes_fee = float(request.form['boxes_fee'])
        market_loader = float(request.form['market_loader'])
        weight_lost = float(request.form['weight_lost'])
        fuel = float(request.form['fuel'])
        others = float(request.form['others'])
        total_quantity  = 0

        # running checks
        if product_id is None or product_id == "":
            flash('You must put a Name!', category="error")
            return render_template("add_fee.html", fees_active=True)
        
        product_obj = storage.get(Product, product_id)
        
        for order in product_obj.orders:
            total_quantity += order.quantity
        product_obj.stock =  product_obj.primary_stock - (total_quantity + weight_lost)
        product_obj.save()
        
        
        total_cost = warehouse_loader + cutting + to_market + gaz + boxes_fee + market_loader + fuel + others
        price_per_unit = (total_cost + (product_obj.unit_price * product_obj.primary_stock )  ) / (product_obj.primary_stock - weight_lost )


        # creating the new product and saving it to the datadase
        new_fee = Fee()
        new_fee.product_id = product_id
        new_fee.warehouse_loader = warehouse_loader
        new_fee.boxes_fee = boxes_fee
        new_fee.market_loader = market_loader
        new_fee.cutting = cutting
        new_fee.user_id = current_user.id
        new_fee.to_market = to_market
        new_fee.weight_lost = weight_lost
        new_fee.gaz = gaz
        new_fee.fuel = fuel
        new_fee.others = others
        new_fee.total_cost = total_cost
        new_fee.price_per_unit = price_per_unit

        new_fee.save()
        return redirect('/fees')
    
@views.route('/fees')
@login_required
def fees():
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

    boxes_out = 0
    for client in clients:
        boxes_out += client.boxes_number 
   # geting the boxes out number
    boxes = current_user.boxes_in
    fees = storage.session.query(Fee).filter_by(user_id=current_user.id).order_by(desc(Fee.created_at)).all()

    # creating the statinfo data list to display in the dashboard

    statsinfo = [len(products), len(orders), revenue, len(clients),boxes_out]
    # stats data end
    feeList = []
    obj = {}
    for fee in fees:
        obj["product_name"] = storage.get(Product, fee.product_id).name
        obj["price_per_unit"] = fee.price_per_unit
        obj["total_cost"] = fee.total_cost
        obj["weight_lost"] = fee.weight_lost
        obj["id"] = fee.id
        obj["created_at"] = fee.created_at
        feeList.append(obj.copy()) # copy to prevent overwriting the object
    return render_template("fees.html", statsinfo=statsinfo, fees_active=True, fees=feeList)
# the route for the product info page
@views.route('/fee_info/<fee_id>')
@login_required
def fee_info(fee_id):
    # getting the product with the id passed in the request

    fee = storage.get(Fee, fee_id)
    if fee is None:  # checking if the product with id=product_id exists
        return render_template('404.html'), 404
    if current_user.id != fee.user_id:  # checking if user is the owner of the product
        flash('An error has occurred!', category="error")

    # getting all the orders of the product and calculating the total revenue
    product_name = storage.get(Product, fee.product_id).name

    return render_template("fee_info.html", fees_active=True, fee=fee, product_name = product_name)


# the route for editing a product
@views.route('/edit_fee/<fee_id>', methods=['GET', 'POST'])
@login_required
def edit_fee(fee_id):
    # getting the product with the id passed in the request

    fee = storage.get(Fee, fee_id)
    products = current_user.products
    if fee is None:  # checking if the product with id=product_id exists
        return render_template('404.html'), 404
    if current_user.id != fee.user_id:  # checking if user is the owner of the product
        flash('An error has occurred!', category="error")
    if request.method == 'POST':
        # if POST requesting, get the fields, check them and edit the product
        product_id = fee.product_id
        warehouse_loader = float(request.form['warehouse_loader'])
        cutting = float(request.form['cutting'])
        to_market = float(request.form['to_market'])
        gaz = float(request.form['gaz'])
        boxes_fee = float(request.form['boxes_fee'])
        market_loader = float(request.form['market_loader'])
        weight_lost = float(request.form['weight_lost'])
        fuel = float(request.form['fuel'])
        others = float(request.form['others'])
        total_quantity  = 0
        # running checks
        if product_id is None or product_id == "":
            flash('You must put a Name!', category="error")
            return render_template("edit_fee.html", fees_active=True)
        
        product_obj = storage.get(Product, product_id)
        product_name = product_obj.name
        
        
        for order in product_obj.orders:
            total_quantity += order.quantity
        product_obj.stock =  product_obj.primary_stock - (total_quantity + weight_lost)
        product_obj.save()
        
        
        total_cost = warehouse_loader + cutting + to_market + gaz + boxes_fee + market_loader + fuel + others
        price_per_unit = ((total_cost + (product_obj.unit_price * product_obj.primary_stock )  )/ (product_obj.primary_stock - weight_lost))

        fee.warehouse_loader = warehouse_loader
        fee.boxes_fee = boxes_fee
        fee.market_loader = market_loader
        fee.cutting = cutting
        fee.user_id = current_user.id
        fee.to_market = to_market
        fee.weight_lost = weight_lost
        fee.gaz = gaz
        fee.fuel = fuel
        fee.others = others
        fee.total_cost = total_cost
        fee.price_per_unit = price_per_unit

        fee.save()
        return redirect(url_for('views.fee_info', fee_id=fee_id))
    # if GET requesting, render the page with the form of editing the product
    fee = storage.get(Fee, fee_id)
    product_id = fee.product_id
    product = storage.get(Product, product_id)
    
    return render_template("edit_fee.html", fees_active=True, fee=fee,product = product)

# List of clients with boxes_to return
@views.route('/boxes_client/')
@login_required
def boxes_client():
    # getting the product with the id passed in the request
    clients = storage.session.query(Client).filter_by(user_id=current_user.id).order_by(desc(Client.boxes_number)).all()
    orders = current_user.orders
    
    
    # Loading all the orders in the wanted format



    results = []

    for client in clients:
        if client.boxes_number > 0:
            orders = sorted(client.orders, key=lambda k: k.created_at, reverse=True)
            if orders:
                latest_order = orders[0]
                delay = (datetime.utcnow() - latest_order.created_at).days
                results.append((client, latest_order.created_at, delay))
            else:
                # If no orders, you can set default values or handle it as needed
                results.append((client, None, None))

    return render_template("boxes_client.html", clients_active=True, clients=results)

# the route for deleting a product
@views.route('/delete_fee/<fee_id>')
@login_required
def delete_fee(fee_id):
    # getting the product with the id passed in the request
    fee = storage.get(Fee, fee_id)
    if fee is None:  # checking if the product with id=product_id exists
        return render_template('404.html'), 404
    if current_user.id != fee.user_id:  # checking if user is the owner of the product
        flash('An error has occurred!', category="error")
        return redirect('/')
    
    # deleting the product using the BaseModel.delete() method
    fee.delete()
    storage.save()
    # show the success message
    flash('fee has been deleted!', category="success")
    return redirect('/')