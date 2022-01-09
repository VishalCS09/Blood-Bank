from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'a' 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'internal'
mysql = MySQL(app)
@app.route('/')
def signup():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM account WHERE Email = % s', (username, ))
        account = cursor.fetchone()
        print(account)
    return render_template('login.html', msg = msg)
if __name__ == '__main__':
   app.run(debug=True, host = "0.0.0.0",port = 8080)# -*- coding: utf-8 -*-
