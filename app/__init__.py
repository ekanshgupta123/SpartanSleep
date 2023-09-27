from flask import Flask

spartan_app = Flask(__name__)
spartan_app.static_url_path = '/static'
spartan_app.static_folder = 'static'

from app import routes