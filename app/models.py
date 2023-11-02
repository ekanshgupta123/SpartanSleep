from app import db
from datetime import datetime
from flask_login import login_manager
from app import login
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(256), nullable=False, unique=True)
    lastName = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    # Relationships
    booked = db.relationship('Booked', backref='user', lazy=True)
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Payment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    expiry_date = db.Column(db.String(10), nullable=False)
    cvv = db.Column(db.String(4), nullable=False)

    # Relationships
    booked = db.relationship('Booked', backref='payment', uselist=False)

class Booked(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    hotelName = db.Column(db.String(100), nullable=False)
    hotelRoomName = db.Column(db.String(100), nullable=False)
    hotelRooms = db.Column(db.Integer, nullable=False)
    totalGuests = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False, unique=True)