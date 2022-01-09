
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

app = Flask(__name__)
app.secret_key = 'a' 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blood'
mysql = MySQL(app)
@app.route('/')
def intro():
    return render_template('index.html')
@app.route('/signup',methods=['GET','POST'])
def signup():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM account WHERE email = % s', (email, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO account VALUES (NULL, % s, % s, % s)', (username,email,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            body=" Hello {} \n\n Welcome to Blood. We're thrilled to see you here!\n your efforts to help those in need are much  appreciated \n stay Healthy\n Best\n Blood".format(username)
            subject="Donate Blood"
            message=MIMEMultipart()
            message['From']="crackpython21@gmail.com"
            message['To']=email
            message['subject']=subject
            message.attach(MIMEText(body,'plain'))
            text=message.as_string()
            mail=smtplib.SMTP('smtp.gmail.com', 587)
            mail.starttls()
            mail.login("crackpython21@gmail.com","python@21")
            mail.sendmail("crackpython21@gmail.com",email,text)
            mail.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
            
    return render_template('signup.html',msg=msg) 
@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg = '' 
    if request.method=='POST' :
        email = request.form['email']
        password = request.form['password']
        print(email ,password)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM account WHERE email = % s AND password = % s', (email, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['email'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('bloodstock.html')
        else:
            msg = 'Incorrect username / password !'
        return render_template('login.html', msg = msg)
    return render_template('login.html', msg = msg)
@app.route('/bloodstock',methods=['GET','POST'])
def bloodstock():
    msg=" "
    if request.method=='POST' :
        username = request.form['username']
        email=request.form['email']
        bloodtype = request.form.get('bloodtype', False)
        print(email ,bloodtype,username)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM donate  WHERE bloodtype  = % s', (bloodtype ,))
        account = cursor.fetchone()
        if account:
            print (account)
            msg="Available"
            return render_template('bloodstock.html',msg=msg)
        else:
             msg="Not Available"
             return render_template('bloodstock.html',msg=msg)
    return render_template('bloodstock.html',msg=msg)

@app.route('/Donate',methods=['GET','POST'])
def donate():
    msg=" "
    if request.method=='POST' :
        username = request.form['username']
        email=request.form['email']
        gender=request.form.get('gender', False)
        age=request.form.get('age', False)
        phoneno= request.form.get('number',False)
        bloodtype = request.form.get('bloodtype', False)
        city= request.form.get('city',False)
        print(username,email,gender,age,phoneno,bloodtype,city)
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO donate VALUES (NULL, % s, % s, % s,% s, % s, % s ,%s )', (username,email,gender,age,phoneno,bloodtype,city))
        mysql.connection.commit()
        msg="sucessfull"
    return render_template('donate.html',msg=msg)

@app.route('/donorinfo',methods=['GET','POST'])
def donorinfo():
    
    return render_template('donorinfo.html')

@app.route('/modify',methods=['GET','POST'])
def modify():
    msg=" "
    if request.method=='POST' :
        email=request.form['email']
        print(email)
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM donate WHERE email=%s',(email,))
        mysql.connection.commit()
        msg="DELETED SUCESSFULLY"
    return render_template('modify.html',msg=msg)
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email')
   return render_template('index.html')

if __name__ == '__main__':
   app.run(debug=True, host = "0.0.0.0",port = 8080)# -*- coding: utf-8 -*-


