from app import spartan_app, mysql
from flask import render_template
from flask import request, url_for, redirect

@spartan_app.route('/',methods=['Get','Post'])
def homePage():
    return render_template('index.html')

@spartan_app.route('/login',methods=['Get','Post'])
def login():
    return render_template('login.html')


@spartan_app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Account (email, firstName, lastName, pass) VALUES (%s, %s, %s, %s)',
                       (email, first_name, last_name, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('homePage'))