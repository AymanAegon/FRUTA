from flask import Blueprint, render_template

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