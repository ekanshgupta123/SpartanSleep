from app import spartan_app, db
from flask import render_template, redirect, flash, request, url_for, session, jsonify
from app.forms import SignupForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from flask import render_template
from datetime import timedelta
import datetime
import subprocess
import os
import time
import hashlib
import requests


#api information for hotelbeds
api_key = "7e71a1cf29aebcaed738be43eb126e12"
secret = "d0050074ba"
datenow = str(datetime.datetime.now().timestamp())
datenow = bytes(datenow, 'utf-8')

string= str(api_key).strip()+str(secret).strip()+str(int(time.time())).strip()

signature= hashlib.sha256(string.encode()).hexdigest()

headers = {
    'Accept': 'application/json',
    'Api-key': api_key,
    'X-Signature': signature,
}

#database initialization
@spartan_app.before_request
def before_request():
    session.permanent = True
    spartan_app.permanent_session_lifetime = timedelta(minutes=15) 

@spartan_app.before_first_request
def create_tables():
    db.create_all()


#homepage path
@spartan_app.route('/', methods=['GET','POST'])
def homePage():
    return render_template('index.html')

@spartan_app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None and not user.verify_password(form.password.data):
            flash("Wrong password or email")
            return redirect(url_for('login'))
        login_user(user,form.remember_me.data)
        print(form.email.data, form.password.data)
        return redirect(url_for('homePage'))
    return render_template('login.html',form=form,authorized=current_user.is_authenticated)

@spartan_app.route("/logout")
def logout():
    db.session.commit()
    logout_user()
    return redirect('/login')


#checking to see if api is up
@spartan_app.route('/execute_script', methods=['GET'])
def execute_script():
    # print(signature)

    # Replace with the actual API endpoint
    url = 'https://api.test.hotelbeds.com/hotel-api/1.0/status'

    # Make the API request
    return requests.get(url, headers=headers).json()


#show hotels path
@spartan_app.route('/hotels')
def hotel():
    url = "https://api.test.hotelbeds.com/hotel-content-api/1.0/hotels"

    hotel_codes = [1, 2]

    query_params = {
        "codes": ",".join(map(str, hotel_codes)),
        # "apikey": api_key,
    }

    response = requests.get(url, headers = headers, params=query_params)


    images = []
    if response.status_code == 200:
        hotel_images = {}  # Create a dictionary to associate images with hotels

        hotel_data = response.json()

        # Get the list of hotels
        hotels = hotel_data.get("hotels")

        hotel_images = {}  # Create a dictionary to associate images with hotels


        if hotels:
            for hotel in hotels:
                hotel_code = hotel.get("code")
                images = hotel.get("images")
                
                if hotel_code and images:
                    # Add images to the corresponding hotel in the dictionary
                    if hotel_code not in hotel_images:
                        hotel_images[hotel_code] = []
                    hotel_images[hotel_code].extend(images)
        
        hotel_path_dict = {}
        baseUrl = "http://photos.hotelbeds.com/giata/"

        for hotel_key, images_list in hotel_images.items():
            hotel_image_paths = []
            
            # Iterate through the list of images for this hotel
            for image in images_list:
                path = baseUrl + image.get("path")  # Access the "path" key in each image dictionary
                hotel_image_paths.append(path)
            
            # Add the list of image paths to the dictionary with the hotel key as the key
            hotel_path_dict[hotel_key] = hotel_image_paths

        for key, img in hotel_path_dict.items():
            print(key, img)
        return hotel_path_dict
    else:
        # Handle the case where the API request failed
        print(f"API request failed with status code {response.status_code}")
        print(response.text)
        error_response = jsonify({"error": "API request failed"}), 500  # Create an error response as JSON with status code 500
        return error_response


#sign up path
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







