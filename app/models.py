from app import db
from datetime import datetime
from flask_login import login_manager
from app import login
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(256), nullable=False, unique=True)
    lastName = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Payment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    expiry_date = db.Column(db.String(10), nullable=False)
    cvv = db.Column(db.String(4), nullable=False)
    start_date = db.Column(db.String(10), nullable=False)
    end_date = db.Column(db.String(10), nullable=False)
    hotelName = db.Column(db.String, nullable=False)
    hotelRooms = db.Column(db.Integer, nullable=False)
    totalGuests = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user = relationship("User", backref="payments")





