from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return 'logout'

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) < 4:
            flash('Username must be greater than 4 characters!', category="error")
        elif len(email) < 5:
            flash('Email must be greater than 5 characters!', category="error")
        elif len(password1) < 8:
            flash('Password must be greater than 8 characters!', category="error")
        elif password1 != password2:
            flash('Passwords don\'t match', category="error")
        else:
            # add new user
            flash('Account created!', category="success")
    return render_template("sign_up.html")