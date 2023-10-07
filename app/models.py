from app import db
from datetime import datetime
from flask_login import login_manager
from app import login

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(256), nullable=False, unique=True)
    lastName = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
