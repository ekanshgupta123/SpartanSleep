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
    reward_points = db.Column(db.Integer, default=0)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Payment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    card_number = db.Column(db.String(16), nullable=False, default='1234567812345678')
    expiry_date = db.Column(db.String(10), nullable=False, default='01/23')
    cvv = db.Column(db.String(4), nullable=False, default='123')
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)
    hotelName = db.Column(db.String, nullable=False)
    hotelRooms = db.Column(db.Integer, nullable=False)
    totalGuests = db.Column(db.Integer, nullable=False)
    cityCode = db.Column(db.String, nullable=False)
    countryCode = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    user = relationship("User", backref="payments")

class Rewards(db.Model, UserMixin):
    id =db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reward_points = db.Column(db.Integer)

    user = relationship("User", backref="rewards")




