from flask import Flask
from flask_login import LoginManager
from models.user import User
from models import storage

def create_app():
    """
    a function to create the flask app

    Returns:
        flsak app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hghghghg'

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return storage.get(User, id)

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app