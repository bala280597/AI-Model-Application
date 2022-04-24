from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import joblib
import numpy as np
from forms import HouseForm

app = Flask(__name__)
app.secret_key = 'Bala@123'

app.config['MYSQL_HOST'] = '34.136.215.194'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Bala@123'
app.config['MYSQL_DB'] = 'aiml'

mysql = MySQL(app)

@app.route('/')
def hello():
	return "Hello World"

@app.route("/predict", methods=["GET"])
def predict():
    house_form = HouseForm()
    if house_form.validate_on_submit():
        Avg_Area_Income = float(house_form.Avg_Area_Income.data)
        Avg_Area_House_Age = float(house_form.Avg_Area_House_Age.data)
        Avg_Area_Number_of_Rooms = float(house_form.Avg_Area_Number_of_Rooms.data)
        Avg_Area_Number_of_Bedrooms = float(house_form.Avg_Area_Number_of_Bedrooms.data)
        Area_Population = float(house_form.Area_Population.data)

    return render_template("car.html", form=house_form)

@app.route("/predict", methods=["POST"])
def result():
    try:
        form = request.form
        model = joblib.load("aiml/house.pkl")

        new_house = np.array(
            [float(form['Avg_Area_Income']), float(form['Avg_Area_House_Age']),
             float(form['Avg_Area_Number_of_Rooms']), float(form['Avg_Area_Number_of_Bedrooms']), float(form['Area_Population'])
            ]).reshape(1, -1)
        predicted_price = model.predict(new_house)
        if predicted_price < 0:
            predicted_price = 0
        return render_template("result.html", price=int(predicted_price))
    except ValueError:
        return render_template("error.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM login WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			add_app = ("INSERT into pricing "
					   "(username)"
					   "VALUES (%(username)s )")
			data_app = {
				'username': account['username']
			}
			cursor.execute(add_app, data_app)
			mysql.connection.commit()
			return redirect(url_for('predict'))
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM login WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO login VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

if __name__ == '__main__':
  app.run(host = "0.0.0.0",port=7001)
