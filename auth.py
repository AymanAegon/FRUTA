from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from models import storage
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# the route for login a user
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # if method is post, get email and password 
        email = request.form.get('email')
        password = request.form.get('password')
        # getting the user with email
        user = None
        users = storage.all(User).values()
        for obj in users:
            if obj.email == email:
                user = obj
                break
        if user is None: # checking if user with the email exists
            flash('User with this email does not exist!', category="error")
        elif check_password_hash(user.password, password) is False: # checking if the password correct
            flash('Incorrect password, Try again!', category="error")
        else:
            # login the user
            flash('Logged in successfully!', category="success")
            login_user(user, remember=True)
            return redirect(url_for('views.products'))
    # if method is get, reder the login form
    return render_template("login.html")

# the route for Logging out a user
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('auth.login')

# the route for Signing up a new user
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
            # Creating a new user object and save it into the DB
            new_user = User()
            new_user.name = name
            new_user.email = email
            # storing a hash password
            new_user.password = generate_password_hash(password1, method="scrypt")
            new_user.save()
            flash('Account created!', category="success")
            login_user(new_user, remember=True)
            return redirect(url_for('views.products'))
    return render_template("sign_up.html")