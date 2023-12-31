# -----------------------------------------------------------
# Project: BeatBank
# File: __init__.py
# Descritption: This is the init.py file for the app package. It is the
# first file that is run when the app is started. It contains
# all of the app's initialization code, including the
# creation of the Flask app object, the SQLAlchemy database
# object, and the Flask login manager object. It also
# initializes the Flask cache object.
#
# Author: Parker Tonra
# -----------------------------------------------------------

from flask import Flask
import os
from flask_migrate import Migrate
from flask_mail import Mail
from sqlalchemy.orm.exc import NoResultFound

app = Flask("Beat Layer")
app.secret_key = os.environ['SECRET_KEY']
app.template_folder = 'src/templates'
app.static_folder = 'src/static'

# db initialization
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beatbank.db'
db.init_app(app)

from src.app import models
with app.app_context():
    db.create_all()

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from src.app.config import Config
mail = Mail(app)

from src.app.models import User


# user_loader callback
@login_manager.user_loader
def load_user(id):
    try:
        return db.session.query(User).filter(User.id == id).one()
    except NoResultFound:
        return None


# cache setup
from flask_caching import Cache
cache = Cache()
cache.init_app(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

from src.app import routes
