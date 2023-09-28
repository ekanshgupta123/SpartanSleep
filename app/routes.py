from app import spartan_app
from flask import render_template

@spartan_app.route('/base',methods=['Get','Post'])
def homePage():
    return render_template('index.html')

@spartan_app.route('/login',methods=['Get','Post'])
def login():
    return render_template('login.html')
