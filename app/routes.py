from app import spartan_app, db
from flask import render_template, redirect, flash, request, url_for, session
from app.forms import SignupForm
from app.models import User
from flask import render_template
from datetime import timedelta


@spartan_app.before_request
def before_request():
    session.permanent = True
    spartan_app.permanent_session_lifetime = timedelta(minutes=15) 

@spartan_app.before_first_request
def create_tables():
    db.create_all()


@spartan_app.route('/', methods=['GET','POST'])
def homePage():
    return render_template('index.html')

@spartan_app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@spartan_app.route('/signup', methods=['GET', 'POST'])
def signup():
    current_form = SignupForm()
    if current_form.validate_on_submit():
        user = User(
            firstName=current_form.firstName.data,
            lastName=current_form.lastName.data,
            email=current_form.email.data,
            password=current_form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account creation successful!')
        return redirect(url_for('login'))
    return render_template('signup.html', form=current_form)







