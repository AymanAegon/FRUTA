from create_app import create_app
from flask import render_template
from flask_login import LoginManager
from models.user import User
from models import storage

app = create_app()

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(id):
    return storage.get(User, id)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)