from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from jinja2 import Environment

spartan_app = Flask(__name__)
spartan_app.static_url_path = '/static'
spartan_app.static_folder = 'static'

basedir = os.path.abspath(os.path.dirname(__file__))

spartan_app.config.update(
    SECRET_KEY='this-is-a-secret',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),   #sets location of database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(spartan_app)
migrate = Migrate(spartan_app,db)


from app import routes