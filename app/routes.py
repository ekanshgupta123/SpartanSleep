from app import spartan_app, db
from flask import render_template, redirect, flash, request, url_for, session, jsonify
from app.forms import SignupForm, SearchForm
from app.forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from datetime import timedelta
import pycountry
import requests

#database initialization
@spartan_app.before_request
def before_request():
    session.permanent = True
    spartan_app.permanent_session_lifetime = timedelta(minutes=15) 

@spartan_app.before_first_request
def create_tables():
    db.create_all()


# homepage path
@spartan_app.route('/', methods=['GET','POST'])
def homePage():
    return render_template('index.html')

# login path
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

# logout path
@spartan_app.route("/logout")
def logout():
    db.session.commit()
    logout_user()
    return redirect('/login')

@spartan_app.route('/delete/<int:id>')
def delete(id):
    # attempt to get the user by provided id, and if it doesn't exist -> return 404 error
    user = User.query.get_or_404(id)

    try:
        # Delete the user from the database:
        db.session.delete(user)
        db.session.commit()

        # Redirect the user to the home page:
        return redirect(url_for('home'))
    except:
        # If there was 1 error while deleting the user's account, display 1 error message:
        return 'There was something wrong when deleting your account!'
    
#getting request token
def get_access_token():
    global access_token

    #api information for amadeus
    client_id = 'eLWoFfHf0ngMXRZoClATedEWUIRAsFDB'
    client_secret = '0oEEu6nk1da8MqeF'
    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        # Parse the JSON response to get the access token
        access_token = response.json()["access_token"]
        return access_token
    else:
        return None

# seeing if api is up
# @spartan_app.route('/execute_script', methods=['GET', 'POST'])
# def execute():
#     access_token = get_access_token()

#     if access_token:
#         return jsonify({"access_token": access_token})
#     else:
#         return jsonify({"error": "Failed to obtain access token"})

# sign up path
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


# home path
@spartan_app.route("/home")
@login_required
def home():
    if(current_user.is_authenticated):
        return render_template('home.html', authorized=current_user.is_authenticated)
    return render_template('home.html', authorized=current_user.is_authenticated)


# search for cities
@spartan_app.route('/search', methods=['POST'])
def search():

    search_term = request.form.get('text', '').strip()
    
    # Check if the search term is empty
    if not search_term:
        return jsonify([])  # Return an empty list if no search term is provided
    
    # Define the Amadeus API endpoint and API key
    amadeus_api_url = f"https://test.api.amadeus.com/v1/reference-data/locations/cities?keyword={search_term}&max=10"
    
    # Set up headers with the API key
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    try:
        # Send a GET request to the Amadeus API
        response = requests.get(amadeus_api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            cities = data.get('data', [])
            
            city_and_country = []  # Create a list to store city and country info
            
            for city in cities:
                city_name = city['name']
                country_code = city['address']['countryCode']
                country_name = pycountry.countries.get(alpha_2=country_code).name
                
                city_and_country.append({"city": city_name, "country": country_name})
            
            return jsonify(city_and_country)  # Return city and country info as JSON
        else:
            return jsonify([])  # Return an empty list if there's an issue with the API
    except Exception as e:
        print(f"Error fetching data from Amadeus API: {e}")
        return jsonify([])  # Return an empty list in case of an error


# rooms path

# about us path
@spartan_app.route('/about')
def aboutUs():
    return render_template('about.html')

# profile path
