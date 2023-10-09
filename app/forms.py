from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from flask import flash
from app.models import User


class SignupForm(FlaskForm):
    #creating fields for signing up
    email = StringField('Email', validators=[DataRequired(message="Email required.")])
    firstName = StringField('First Name', validators=[DataRequired(message="First Name required.")])
    lastName = StringField('last Name', validators=[DataRequired(message="Last Name required.")])
    password = PasswordField('Password', validators=[DataRequired(message="Password required."), Length(min=8, message="Password must be more than 8 characters long")])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password must match.')])
    submit = SubmitField('Sign Up')
    
    #validate username to see if there is already that user name in the database; ensure unique username
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:        #username matches with one in a database
            raise ValidationError("Username already taken.")
        
    #validate email to ensure unique email
    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email is not None:        #email matches with one in a database
            raise ValidationError("Email already taken.")

class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit=SubmitField('Sign in')

class SearchForm(FlaskForm):
    #creating fields for searching
    searchInput = StringField('Search For User', validators = [DataRequired()])


