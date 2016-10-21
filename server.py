import psycopg2
import psycopg2.extras
import os
import uuid
import db
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

passed = False
name = ''

@app.route('/')
def mainIndex():
    global name
    global passed
    if passed:
        session['username'] = name
        name = ''
        passed = False
    
    session['loginRequired'] = True
    if 'username' in session:
        session['loginRequired'] = False

        
    return render_template('index.html', current='home', loginRequired= session['loginRequired'])

@app.route('/category')
def ourWork():
    productList= [{'name':'Electronics', 'description':'Best iphone ever created','image':'home_1.jpg'},
                    {'name':'Furniture', 'description':'Best iphone ever created','image':'home_1.jpg'}]
    return render_template('category.html', current='category', productList = productList)

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html',current='testimonials', title=title)

@app.route('/projects')
def projects():
    return render_template('projects.html',current='projects', title=title)

@app.route('/contact')
def contact():
    return render_template("contact.html",current='contact', title=title)

@app.route('/electronics')
def electronics():
    queryFetch = db.productsList('electronics')
    print queryFetch
    return render_template("product.html", queryFetch=queryFetch)
    
@app.route('/furniture')
def furniture():
    queryFetch = db.productsList('furniture')
    print queryFetch
    return render_template("product.html", queryFetch=queryFetch)
    
##########################################SocketIO STUFF ###########################################
###################Login################
@socketio.on('login', namespace='/eCom')
def login(username, password):
    global passed
    global name
    loginQueryFetch = db.login(username, password)
    if loginQueryFetch is None:
        emit('loginFailed','Invalid Username', namespace='/eCom')
        print 'how many times we are coming in if of loginPageValidation---------------------------------'
    else:
        #session['username'] = username
        #session['loginRequired'] = False
        passed = True
        name = username
        print(session['loginRequired'])
        emit('redirect',"/", namespace='/eCom')
        print 'how many times we are coming in else of loginPageValidation---------------------------------'
            #return render_template('index.html')

################register#################    
@socketio.on('register', namespace='/eCom')
def register(username, firstName, lastName, password, conPassword, address, city,state, zip, country, email):
    
    userCheck = db.checkUserNameExist(username)
    if len(userCheck) > 0:
        print('user name is already taken')
        emit('regFail', 'Username already taken!')
    else:
        if password != conPassword:
            emit('regFail', 'Passwords do not match!')
        else:
            db.registerIntoDb(username, firstName, lastName, password, conPassword, address, city,state, zip, country, email)
            emit('redirect',"/", namespace='/eCom')

    
# start the server
if __name__ == '__main__':
        socketio.run(app,host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
    