from app import spartan_app, db
from flask import render_template, redirect, flash, request, url_for, session, jsonify
from app.forms import SignupForm, SearchForm
from app.forms import LoginForm
from app.forms import PaymentForm
from app.forms import RewardsForm
from app.models import User
from app.models import Payment
from app.models import Rewards
from flask_login import login_user, logout_user, login_required, current_user
from datetime import timedelta
import pycountry
import requests
import random
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import time

#database initialization
@spartan_app.before_request
def before_request():
    session.permanent = True
    spartan_app.permanent_session_lifetime = timedelta(minutes=15) 

#@spartan_app.before_first_request
#def create_tables():
with spartan_app.app_context():
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
        if user is None:
            flash("Wrong email")
            return redirect(url_for('login'))
        else:
            if not check_password_hash(user.password, form.password.data):
                flash("Wrong password")
                return redirect(url_for('login'))
        login_user(user,form.remember_me.data)
        print(form.email.data, form.password.data)
        return redirect(url_for('homePage'))
    return render_template('login.html',form=form,authorized=current_user.is_authenticated)

# logout path
@spartan_app.route("/logout")
@login_required
def logout():
    db.session.commit()
    logout_user()
    return redirect('/login')

@spartan_app.route('/delete/<int:id>')
@login_required
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
        hashed_password=generate_password_hash(current_form.password.data)
        user = User(
            firstName=current_form.firstName.data,
            lastName=current_form.lastName.data,
            email=current_form.email.data,
            password=hashed_password
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
@login_required
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
                city_code = city.get('iataCode', 'N/A')  
                country_name = pycountry.countries.get(alpha_2=country_code).name
                
                city_and_country.append({"city": city_name, "country": country_name, "cityCode": city_code})
            return jsonify(city_and_country)  # Return city and country info as JSON
        else:
            return jsonify([])  # Return an empty list if there's an issue with the API
    except Exception as e:
        print(f"Error fetching data from Amadeus API: {e}")
        return jsonify([])  # Return an empty list in case of an error

@spartan_app.route('/hotel-view/<string:hotel_id>', methods = ['GET', 'POST'])
@login_required
def hotel_view(hotel_id):
    amadeus_api_url = f"https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-hotels?hotelIds={hotel_id}"
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    try:
        # Send a GET request to the Amadeus API
        response = requests.get(amadeus_api_url, headers=headers)

        if response.status_code == 200:
            # Extract and process hotel data from the response
            hotel_data = response.json()

            # Extract and process user inputted data from the form
            checkIn = request.args.get('checkIn')
            checkOut = request.args.get('checkOut')
            guests = request.args.get('guests')
            rooms = request.args.get('rooms')
            price = request.args.get('price')

            print(f"checkIn: {checkIn}, checkOut: {checkOut}, guests: {guests}, rooms: {rooms}")

            if isinstance(hotel_data, (dict, list)):
                hotel_data = hotel_data["data"][0]
                print("Hotel Name:", hotel_data['name'])
                return render_template('hotel-view.html', hotel_data=hotel_data, checkIn=checkIn, checkOut=checkOut, guests=guests, rooms=rooms, price=price)
            else:
                return "Invalid hotel data format"
        else:
            response_json = response.json()  # Parse the JSON response
            # return response_json
            if "errors" in response_json and isinstance(response_json["errors"], list):
                error_list = response_json["errors"]

            if error_list:
                first_error = error_list[0]  # Assuming the first error message is what you want
                error_title = first_error.get("title", "Unknown Error")
                print(error_title)  # Print the "title" property
                if (error_title == 'NOTHING FOUND FOR REQUESTED CITY'):
                    return "There are no hotels in the city radius"
                else:
                    return "Some other error occurred"
    except Exception as e:
        print(f"Error fetching hotel data from Amadeus API: {e}")
        return "An error occurred"

# DO NOT USE. NOT ACTIVELY IN USE FOR HOTEL-SEARCH. I THINK WE SHOULD REMOVE THIS.
@spartan_app.route('/hotels/<cityCode>/')
def hotel_search(cityCode):
    # Pass all booked hotels to the template
    booked_hotels = Payment.query.all()
    num_booked_hotels = Payment.query.count()
    print("Number of booked hotels:", num_booked_hotels)  # Add this line for debugging

    # Construct the Amadeus API URL for hotel search based on the city and country
    amadeus_api_url = f"https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city?cityCode={cityCode}&radius=15&radiusUnit=MILE&hotelSource=ALL"

    # Set up headers with the API key
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    try:
        # Send a GET request to the Amadeus API
        response = requests.get(amadeus_api_url, headers=headers)

        if response.status_code == 200:
            # Extract and process hotel data from the response
            hotel_data = response.json()

            if isinstance(hotel_data, (dict, list)):
                return render_template('hotel-search.html', booked_hotels=booked_hotels, num_booked_hotels=num_booked_hotels, hotel_data=hotel_data)
            else:
                return "Invalid hotel data format"
   
            # # Render the hotel search template with the hotel data
            # return render_template('hotel_search.html', hotels=hotel_data)
        else:
            response_json = response.json()  # Parse the JSON response
            # return response_json
            if "errors" in response_json and isinstance(response_json["errors"], list):
                error_list = response_json["errors"]

            if error_list:
                first_error = error_list[0]  # Assuming the first error message is what you want
                error_title = first_error.get("title", "Unknown Error")
                print(error_title)  # Print the "title" property
                if (error_title == 'NOTHING FOUND FOR REQUESTED CITY'):
                    return "There are no hotels in the city radius"
                else:
                    return "Some other error occurred"
    except Exception as e:
        print(f"Error fetching hotel data from Amadeus API: {e}")
        return "An error occurred"

# about us path
@spartan_app.route('/aboutUs')
def aboutUs():
    return render_template('about-us.html')

# profile path

# manage reservations path
@spartan_app.route('/reservations')
@login_required
def reservations():
    user_bookings = db.session.query(Payment.hotelName, Payment.start_date, Payment.end_date, Payment.totalGuests, Payment.hotelRooms, Payment.price, Payment.id, Payment.cityCode, Payment.countryCode,).filter_by(user_id=current_user.id).all()
    print(len(user_bookings))
    return render_template('/reservations.html', user_bookings=user_bookings)

# edit reservations date
@spartan_app.route('/update_reservation_date/<int:reservation_id>', methods=['GET', 'POST'])
@login_required
def update_reservation_date(reservation_id):
    reservation = Payment.query.get(reservation_id)
    checkIn = reservation.start_date
    checkOut = reservation.end_date

    print(f"checkIn: {checkIn}, checkOut: {checkOut}")
    
    if request.method == 'POST':
        new_start_date = request.form.get('new_check_in_date')
        new_end_date = request.form.get('new_check_out_date')  

        if new_start_date is not None and new_end_date is not None:
            try:
                reservation.start_date = datetime.strptime(new_start_date, '%Y-%m-%d').date()
                reservation.end_date = datetime.strptime(new_end_date, '%Y-%m-%d').date()

                db.session.commit()
                flash('Updated Successfully!')
            except ValueError:
                flash('Invalid date format received from the form')
                return redirect(url_for('update_reservation_date', reservation_id=reservation_id))
        else:
            flash('Dates are missing in the form')
            return redirect(url_for('update_reservation_date', reservation_id=reservation_id))
        
        return redirect(url_for('reservations'))

    return render_template('update_reservation_date.html', checkIn = checkIn, checkOut = checkOut)

# hotel-search path
@spartan_app.route('/hotel-search')
@login_required
def hotel_searchs():
#    return render_template('/hotel-search.html')
# Get the value of the "cityCode" query parameter from the request
    cityCode = request.args.get('cityCode')

    # Construct the Amadeus API URL for hotel search based on the city and country
    amadeus_api_url = f"https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city?cityCode={cityCode}&radius=15&radiusUnit=MILE&hotelSource=ALL"

    # Set up headers with the API key
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    # Pass all booked hotels to the template
    booked_hotels = Payment.query.all()
    num_booked_hotels = Payment.query.count()

    try:
        # Send a GET request to the Amadeus API
        response = requests.get(amadeus_api_url, headers=headers)
        print(response.json())
        if response.status_code == 200:
            # Extract and process hotel data from the response
            hotel_data = response.json()
            
            if isinstance(hotel_data, (dict, list)):
                checkIn = request.args.get('date-in')
                checkOut = request.args.get('date-out')
                checkIn_datetime = datetime.strptime(checkIn, "%d %B, %Y").date()
                checkOut_datetime = datetime.strptime(checkOut, "%d %B, %Y").date()

                guests = request.args.get('guest')
                rooms = request.args.get('room')

                return render_template('hotel-search.html', hotel_data=hotel_data, 
                    authorized=current_user.is_authenticated, checkIn=checkIn, checkOut=checkOut, 
                    checkIn_datetime=checkIn_datetime, checkOut_datetime=checkOut_datetime,
                    guests=guests, rooms=rooms, booked_hotels=booked_hotels, num_booked_hotels=num_booked_hotels)
            else:
                return "Invalid hotel data format"
        else:
            response_json = response.json()  # Parse the JSON response
            if "errors" in response_json and isinstance(response_json["errors"], list):
                error_list = response_json["errors"]
                if error_list:
                    first_error = error_list[0]  # Assuming the first error message is what you want
                    error_title = first_error.get("title", "Unknown Error")
                    if error_title == 'NOTHING FOUND FOR REQUESTED CITY':
                        return "There are no hotels in the city radius"
                    else:
                        return "Some other error occurred"
    except Exception as e:
        print(f"Error fetching hotel data from Amadeus API: {e}")
        return "An error occurred"


@spartan_app.route('/book')
def hotel_book():
    url = "https://test.api.amadeus.com/v1"
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }
    obj = {
    "data": {
        "offerId": "NRPQNQBOJM",
        "guests": [
        {
            "name": {
            "title": "MR",
            "firstName": "BOB",
            "lastName": "SMITH"
            },
            "contact": {
            "phone": "+33679278416",
            "email": "bob.smith@email.com"
            }
        }
        ],
        "payments": [
        {
            "method": "creditCard",
            "card": {
            "vendorCode": "VI",
            "cardNumber": "0000000000000000",
            "expiryDate": "2026-01"
            }
        }
        ]
    }
    }
    try:
        response = requests.post(url, headers=headers, json=obj)
        return response.json()
    except Exception as e:
        print(f"Error fetching hotel data from Amadeus API: {e}")
        return "An error occurred"
#display current user rewards
def get_reward_points(user_id):
    user = User.query.get(user_id)
    if user:
        return user.reward_points
    return None
#calculate rewards

@spartan_app.route('/checkout/<string:checkout_type>/<string:hotel_id>', methods=['GET', 'POST'])
@login_required
def checkout(checkout_type, hotel_id):
    amadeus_api_url = f"https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-hotels?hotelIds={hotel_id}"
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    try:
        # Send a GET request to the Amadeus API
        response = requests.get(amadeus_api_url, headers=headers)

        if response.status_code == 200:
            # Extract and process hotel data from the response
            hotel_data = response.json()

            if isinstance(hotel_data, (dict, list)):
                hotel_data = hotel_data["data"][0]
                hotel_name = hotel_data['name']
        else:
            response_json = response.json()  # Parse the JSON response
            # return response_json
            if "errors" in response_json and isinstance(response_json["errors"], list):
                error_list = response_json["errors"]

            if error_list:
                first_error = error_list[0]  # Assuming the first error message is what you want
                error_title = first_error.get("title", "Unknown Error")
                print(error_title)  # Print the "title" property
                if (error_title == 'NOTHING FOUND FOR REQUESTED CITY'):
                    return "There are no hotels in the city radius"
                else:
                    return "Some other error occurred"
    except Exception as e:
        print(f"Error fetching hotel data from Amadeus API: {e}")
        return "An error occurred" 

    if checkout_type == "pay-now":
        user_id = current_user.id
        reward_points = get_reward_points(user_id)
        # Logic for Pay Now checkout
        # You can get the start_date, end_date, total_guests, and price from the URL parameters
        start_date_str = request.args.get("checkIn")
        end_date_str = request.args.get("checkOut")
        # Convert dates to DATE() datetime objects
        start_date = datetime.strptime(start_date_str, "%d %B, %Y").date()
        end_date = datetime.strptime(end_date_str, "%d %B, %Y").date()

        total_guests = request.args.get("guests")
        total_rooms = request.args.get("rooms")
        price = request.args.get("price")

        print(f"Pay now checkIn: {start_date}, checkOut: {end_date}, guests: {total_guests}, rooms: {total_rooms}, price: {price}")
        form = PaymentForm()
        if form.validate_on_submit():
            payment = Payment(
                user_id=current_user.id,
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                card_number=form.card_number.data,
                expiry_date=form.expiry_date.data,
                cvv=form.cvv.data,
                start_date=start_date,
                end_date=end_date,
                hotelName=hotel_name,
                hotelRooms=total_rooms,
                totalGuests=total_guests,
                cityCode=hotel_data["iataCode"],
                countryCode=hotel_data["address"]["countryCode"], #{{hotel_data.address.countryCode}}, {{hotel_data.iataCode }}
                price=int(price)  # Convert price to integer
            )
            db.session.add(payment)
            db.session.commit()
            flash('Payment Accepted!')

            current_user.reward_points = (int(reward_points)+100)
            add_rewards = Rewards(user_id=current_user.id, reward_points=reward_points)
            db.session.add(add_rewards)
            db.session.commit()

            flash('Rewards Redeemed Successfully'.format(reward_points))
            return redirect(url_for('reservations'))

        return render_template('checkout-pay-now.html', hotel_id=hotel_id, form=form)
    # using pay-later for rewards
    elif checkout_type == "pay-later":
        user_id = current_user.id
        reward_points = get_reward_points(user_id)

        start_date_str = request.args.get("checkIn")
        end_date_str = request.args.get("checkOut")
        # Convert dates to DATE() datetime objects
        start_date = datetime.strptime(start_date_str, "%d %B, %Y").date()
        end_date = datetime.strptime(end_date_str, "%d %B, %Y").date()

        total_guests = request.args.get("guests")
        total_rooms = request.args.get("rooms")
        price = request.args.get("price")

        print(f"pay later checkIn: {start_date}, checkOut: {end_date}, guests: {total_guests}, rooms: {total_rooms}, price: {price}")

        rewards_form = RewardsForm()
        if rewards_form.validate_on_submit():
            payment = Payment(
                user_id=current_user.id,
                name=rewards_form.name.data,
                email=rewards_form.email.data,
                phone=rewards_form.phone.data,
                start_date=start_date,
                end_date=end_date,
                hotelName=hotel_name,
                hotelRooms=total_rooms,
                totalGuests=total_guests,
                cityCode=hotel_data["iataCode"],
                countryCode=hotel_data["address"]["countryCode"],
                price=int(price)  # Use the actual price obtained from the URL parameter
            )
            db.session.add(payment)
            db.session.commit()

            current_user.reward_points = (int(reward_points)-100)
            add_rewards = Rewards(user_id=current_user.id, reward_points=reward_points)
            db.session.add(add_rewards)
            db.session.commit()

            flash('Rewards Redeemed Successfully'.format(reward_points))
            return redirect(url_for('reservations'))

        return render_template('checkout-pay-later.html', hotel_id=hotel_id,rewards_form=RewardsForm(),reward_points=reward_points)  # Modify as needed

    else:
        # Handle invalid checkout_type
        return "Invalid checkout type"

'''
@spartan_app.route('/checkout/pay-now/<string:hotel_id>', methods=['GET', 'POST'])
def checkoutPayNow(hotel_id):
    amadeus_api_url = f"https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-hotels?hotelIds={hotel_id}"
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    try:
        # Send a GET request to the Amadeus API
        response = requests.get(amadeus_api_url, headers=headers)

        if response.status_code == 200:
            # Extract and process hotel data from the response
            hotel_data = response.json()

            if isinstance(hotel_data, (dict, list)):
                hotel_data = hotel_data["data"][0]
                hotel_name = hotel_data['name']
        else:
            response_json = response.json()  # Parse the JSON response
            # return response_json
            if "errors" in response_json and isinstance(response_json["errors"], list):
                error_list = response_json["errors"]

            if error_list:
                first_error = error_list[0]  # Assuming the first error message is what you want
                error_title = first_error.get("title", "Unknown Error")
                print(error_title)  # Print the "title" property
                if (error_title == 'NOTHING FOUND FOR REQUESTED CITY'):
                    return "There are no hotels in the city radius"
                else:
                    return "Some other error occurred"
    except Exception as e:
        print(f"Error fetching hotel data from Amadeus API: {e}")
        return "An error occurred"

    # Logic for Pay Now checkout
    # we will need to get the start_date, end_date, total_guests, and price through parameters (it is hard coded right now)
    form = PaymentForm()
    if form.validate_on_submit():
        payment = Payment(
            user_id = current_user.id,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            card_number=form.card_number.data,
            expiry_date=form.expiry_date.data,
            cvv=form.cvv.data,
            start_date = '11/12/2023',
            end_date = '12/12/2023',
            hotelName = hotel_name,
            hotelRooms = 1,
            totalGuests = 1,
            price = 100
        )
        db.session.add(payment)
        db.session.commit()
        flash('Payment Accepted!')
        return redirect(url_for('confirmBooking'))
    return render_template('checkout-pay-now.html', hotel_id=hotel_id, form=PaymentForm())

@spartan_app.route('/checkout/pay-later/<string:hotel_id>')
def checkoutPayLater(hotel_id):
    # Logic for Pay Later checkout
    return render_template('checkout-pay-later.html', hotel_id=hotel_id)
'''
@spartan_app.route('/confirm-booking')
@login_required
def confirmBooking():
    # Logic for Pay Later checkout
    return render_template('confirm-booking.html')


@spartan_app.route('/delete-reservation/<int:payment_id>', methods=['POST'])
def delete_reservation(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    if payment.user_id != current_user.id:
        # Prevent deletion if the current user does not own the reservation
        return jsonify({'error': 'Unauthorized to delete this reservation'}), 401

    try:
        db.session.delete(payment)
        db.session.commit()
        return redirect(url_for('reservations'))
    except Exception as e:
        return jsonify({'error': 'There was a problem deleting the reservation: ' + str(e)}), 500
