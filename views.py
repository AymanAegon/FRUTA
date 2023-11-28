from flask import Blueprint, render_template, request, redirect
from models import storage
from models.client import Client

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html", home_active=True)

@views.route('/orders')
def orders():
    return render_template("orders.html", orders_active=True)

@views.route('/clients')
def clients():
    clients = storage.all("Client").values()
    return render_template("clients.html", clients_active=True, clients=clients)

@views.route('/blank')
def blank():
    return render_template("blank.html")

@views.route('/create_client', methods=['GET', 'POST'])
def create_client():
    if request.method == 'GET':
        return render_template("create_client.html", create_client=True)
    else:
        # all_objs = storage.all()
        new_client = Client()
        new_client.name = request.form['client_name']
        new_client.tel_number = request.form['phone_number']
        new_client.save()
        return redirect('/clients')