from app import spartan_app
from flask import render_template

@spartan_app.route('/')
def homePage():
    return render_template('index.html')
