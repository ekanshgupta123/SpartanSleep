from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from jinja2 import Environment
import os.path
from flask_bcrypt import Bcrypt

basedir = os.path.abspath(os.path.dirname(__file__))

spartan_app = Flask(__name__)
spartan_app.static_url_path = '/static'
spartan_app.static_folder = 'static'

spartan_app.config.update(
    SECRET_KEY='this-is-a-secret',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),#sets location of database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)
spartan_app.config['SQLALCHEMY_BINDS'] = {
    'default': 'sqlite:///' + os.path.join(basedir, 'app.db')#,
    #'payment_db': 'sqlite:///' + os.path.join(basedir, 'payment.db')
}

db = SQLAlchemy(spartan_app)
bcrypt=Bcrypt(spartan_app)
migrate = Migrate(spartan_app,db)


login = LoginManager(spartan_app)
login.login_view = 'login'

from app import routes, models

