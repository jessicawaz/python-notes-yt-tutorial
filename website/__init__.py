from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

# create database
db = SQLAlchemy()
DB_NAME = "database.db"

# initialize flask
def create_app():
    app = Flask(__name__) # name of the file
    app.config['SECRET_KEY'] = 'secret_key'
    # configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # initialize database with our flask app
    db.init_app(app)

    # import routes
    from .views import views
    from .auth import auth

    # register blueprints for routes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # import Models from models.py
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Load user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app # inialize flask finished

# check if db exists, if not create the db
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')