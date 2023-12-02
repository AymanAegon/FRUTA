from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from models import storage
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = None
        users = storage.all(User).values()
        for obj in users:
            if obj.email == email:
                user = obj
                break
        if user is None:
            flash('User with this email does not exist!', category="error")
        elif check_password_hash(user.password, password) is False:
            flash('Incorrect password, Try again!', category="error")
        else:
            flash('Logged in successfully!', category="success")
            login_user(user, remember=True)
            return redirect(url_for('views.products'))
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('auth.login')

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = None
        users = storage.all(User).values()
        for obj in users:
            if obj.email == email:
                user = obj
                break
        if user:
            flash('Email already exists!', category="error")
        elif len(name) < 4:
            flash('Name must be greater than 4 characters!', category="error")
        elif len(email) < 5:
            flash('Email must be greater than 5 characters!', category="error")
        elif len(password1) < 8:
            flash('Password must be greater than 8 characters!', category="error")
        elif password1 != password2:
            flash('Passwords don\'t match', category="error")
        else:
            new_user = User()
            new_user.name = name
            new_user.email = email
            new_user.password = generate_password_hash(password1, method="sha256")
            new_user.save()
            flash('Account created!', category="success")
            login_user(user, remember=True)
            return redirect(url_for('views.products'))
    return render_template("sign_up.html")