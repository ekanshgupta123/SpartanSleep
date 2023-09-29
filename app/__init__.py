from flask import Flask
from flaskext.mysql import MySQL

spartan_app = Flask(__name__)
spartan_app.static_url_path = '/static'
spartan_app.static_folder = 'static'

spartan_app.config['MYSQL_DATABASE_USER'] = 'root'
spartan_app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
spartan_app.config['MYSQL_DATABASE_DB'] = 'SpartanSleep'
spartan_app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(spartan_app)

from app import routes