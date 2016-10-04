import psycopg2
import psycopg2.extras
import os
import uuid
from flask import Flask, session
from flask import Flask,render_template,request
from flask.ext.socketio import SocketIO,emit
from flask import json

from flask import Flask, render_template

#app = Flask(__name__)
app = Flask(__name__, static_url_path='')
app.secret_key=os.urandom(24).encode('hex')
app.config['SECRET_KEY'] = 'secret!'
socketio=SocketIO(app)
title = "Usman IT Services"

def db_connect():
    print 'connection to the db_connect'
    connectionString='dbname=ecom user=usman password=usman host=localhost'
    try:
        print 'are we trying'
        return psycopg2.connect(connectionString)
    except:
        print 'cannot connect to the database'

@app.route('/')
def mainIndex():
    
    packages = {'platinum': '100', 'silver': '300', 'gold':'600'}
    isDiscount = False
    color = {'red', 'orange','green','blue'}
    return render_template('index.html', current='home',title=title, deal=packages, isDiscount=isDiscount, colors=color)

@app.route('/Login')
def ourWork():
    return render_template('login.html', current='ourWork', title=title)

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html',current='testimonials', title=title)

@app.route('/projects')
def projects():
    return render_template('projects.html',current='projects', title=title)

@app.route('/contact')
def contact():
    return render_template("contact.html",current='contact', title=title)

@app.route('/blogpost')
def blogPost():
    return render_template("blogpost.html",current='contact', title=title)
    
@app.route('/videos')
def videos():
    video = [{'title': 'Young Consumers', 'vidLink': 'lSxrAo2lHYQ', 'desc': 'The Rise of India Young Consumers'},
    {'title': 'Mercedes Benz', 'vidLink': 'bzxiM8oxI8I', 'desc': 'Mercedes Benz Service Close to your Heart Commercial'}];

    return render_template('videos.html', title=title, v=video)
    
##########################################SocketIO STUFF ###########################################
@socketio.on('login', namespace='/eCom')
def login(username, password):
    print username 
    print password
    conn=db_connect()
    cur =conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # print(cur.mogrify("select * from users where username=%s and password=%s;",(username11,password11)))
    cur.execute("select * from users where username=%s and password=crypt(%s, password);",(username,password))
    loginQueryFetch=cur.fetchone()
    
    if loginQueryFetch is None:
        emit('loginFailed','Invalid Username', namespace='/eCom')
        print 'how many times we are coming in if of loginPageValidation---------------------------------'
    else:
        emit('redirect',"/", namespace='/eCom')
        print 'how many times we are coming in else of loginPageValidation---------------------------------'
            #return render_template('index.html')
    
@socketio.on('register', namespace='/eCom')
def register(username, firstName, lastName, password, conPassword, address, city,state, zip, country, email):
    print (username, firstName, password, address, city, state, zip, country, email)
    conn = db_connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Check if username already exists
    query = "SELECT username FROM users WHERE username = %s"
    cur.execute(query, [username])
    userCheck = cur.fetchall()
    if len(userCheck) > 0:
        print('user name is already taken')
        emit('regFail', 'Username already taken!')
    else:
        if password != conPassword:
            emit('regFail', 'Passwords do not match!')
        else:
            try:
                queryInsert = "INSERT INTO users(username,password,firstName,lastName,address,city,state,zip,country,email) values (%s,crypt(%s,gen_salt('bf')), %s, %s, %s, %s, %s, %s, %s ,%s);"
                cur.execute(queryInsert,[username, password, firstName, lastName, address, city, state, zip, country, email])
                #print (test)
            except:
                print("ERROR inserting into users")
                print("""INSERT INTO users(username, password, firstName, lastName, address, city, state, zip, country, email)VALUES 
                (%s, crypt(%s, gen_salt('bf')), %s, %s, %s, %s, %s, %s, %s ,%s);""",
                (username, password, firstName, lastName, address, city, state, zip, country, email) )
                conn.rollback()
            conn.commit()
            emit('redirect',"/", namespace='/eCom')

    
# start the server
if __name__ == '__main__':
        socketio.run(app,host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
    