from flask import Blueprint, render_template, request
from models.client import Client

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html", home=True)

@views.route('/orders')
def orders():
    return render_template("orders.html", orders=True)

@views.route('/clients')
def clients():
    return render_template("clients.html", clients=True)

@views.route('/blank')
def blank():
    return render_template("blank.html", blank=True)

@views.route('/create_client', methods=['GET', 'POST'])
def create_client():
    if request.method == 'GET':
        return render_template("create_client.html", create_client=True)
    else:
        new_client = Client()
        new_client.name = request.form['client_name']
        new_client.tel_number = request.form['phone_number']
        new_client.save()
        return render_template("clients.html", clients=True)