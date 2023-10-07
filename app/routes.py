from app import spartan_app, db
from flask import render_template, redirect, flash, request, url_for, session
from app.forms import SignupForm
from app.forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
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
    return render_template('signup.html', form=current_form,authorized=current_user.is_authenticated)

@spartan_app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            flash("Wrong password or email")
            return redirect('/login')
        return redirect('/home')
    return render_template('login.html',form=form,authorized=current_user.is_authenticated)

@spartan_app.route("/logout")
def logout():
    db.session.commit()
    logout_user()
    return redirect('/login')


@spartan_app.route("/home")
@login_required
def home():
    if(current_user.is_authenticated):
        return render_template('home.html', authorized=current_user.is_authenticated)
    return render_template('home.html', authorized=current_user.is_authenticated)
