from flask import Flask, request,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import joblib
import numpy as np
from flask_httpauth import HTTPBasicAuth
from flask import jsonify
import re
import os
import gcsfs
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './auth.json'


app = Flask(__name__)
auth = HTTPBasicAuth()


app.secret_key = os.environ['PASSWORD']
app.config['MYSQL_HOST'] = os.environ['IP']
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = os.environ['PASSWORD']
app.config['MYSQL_DB'] = "aiml"
mysql = MySQL(app)

def load_joblib(bucket_name, file_name):
    fs = gcsfs.GCSFileSystem()
    with fs.open(f'{bucket_name}/{file_name}') as f:
        return joblib.load(f)
@app.route("/", methods=["GET","POST"])    
def hello_world():
    return  jsonify('Hello World')
    
@app.route("/login/predict", methods=["POST"])
@auth.login_required
def result():
    try:
        Avg_Area_Income = float(request.args['Avg_Area_Income'])
        Avg_Area_House_Age = float(request.args['Avg_Area_House_Age'])
        Avg_Area_Number_of_Rooms = float(request.args['Avg_Area_Number_of_Rooms'])
        Avg_Area_Number_of_Bedrooms = float(request.args['Avg_Area_Number_of_Bedrooms'])
        Area_Population = float(request.args['Area_Population'])
        print(Avg_Area_Income, Avg_Area_House_Age,Avg_Area_Number_of_Rooms,Avg_Area_Number_of_Bedrooms,Area_Population)
        #model = joblib.load("aiml/house.pkl")
        model =  load_joblib('aiml_bala', 'model.pkl')
        new_house = np.array([Avg_Area_Income, Avg_Area_House_Age,Avg_Area_Number_of_Rooms,Avg_Area_Number_of_Bedrooms,Area_Population]).reshape(1, -1)
        print(new_house)
        predicted_price = model.predict(new_house)
        print(predicted_price)
        if predicted_price < 0:
            predicted_price = -(predicted_price)
        return jsonify(f"{float(predicted_price)}")
    except ValueError:
        return jsonify(f"{ValueError}")

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    username= request.args['username']
    password= request.args['password']
    email= request.args['email']
    if request.method == 'POST' and username and password and email :
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = % s AND password = % s', (username, password,))
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
    return jsonify(f"{msg}")

@auth.verify_password
def authenticate(username, password):
    if username and password:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            add_app = ("INSERT into pricing " "(username)" "VALUES (%(username)s )")
            data_app = { 'username': account['username'] }
            cursor.execute(add_app, data_app)
            mysql.connection.commit()
            return True
        else:
            return False
    return False

if __name__ == '__main__':
  app.run(host = "0.0.0.0",port=7000)#,ssl_context='adhoc')
