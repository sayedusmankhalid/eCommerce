import psycopg2
import psycopg2.extras
import os
import uuid
import db
from flask import Flask, redirect, url_for, session
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
    un = ""
    if passed:
        session['username'] = name
        name = ""
        passed = False
    
    session['loginRequired'] = True
    if 'username' in session:
        un = session['username']
        session['loginRequired'] = False
    return render_template('index.html', current='home', loginRequired= session['loginRequired'], name = un)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('mainIndex'))

@app.route('/category')
def ourWork():
    global name
    global passed
    un=""
    if passed:
        session['username'] = name
        name = ""
        passed = False
    session['loginRequired'] = True
    if 'username' in session:
        un = session['username']
        session['loginRequired'] = False
    return render_template('category.html', current='category', loginRequired= session['loginRequired'], name = un)

def loginCheck():
    global name
    global passed
    un=""
    new_dict = {'username' : '', 'loginRequired' : False}
    if passed:
        session['username'] = name
        name = ''
        passed = False
    session['loginRequired'] = True
    if 'username' in session:
        un = session['username']
        new_dict['username'] = un
        session['loginRequired'] = False
    new_dict['loginRequired'] = session['loginRequired']
    return new_dict

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html',current='testimonials', title=title)

@app.route('/projects')
def projects():
    return render_template('projects.html',current='projects', title=title)

@app.route('/myProducts')
def myproducts():
    dict = loginCheck()
    username = dict['username']
    queryFetch = db.getMyProducts(username)
    return render_template("product.html", queryFetch=queryFetch, current='myProducts', loginRequired = dict['loginRequired'], name = dict['username'], myPro = True)

@app.route('/contact')
def contact():
    return render_template("contact.html",current='contact', title=title)

@app.route('/electronics')
def electronics():
    dict = loginCheck()
    queryFetch = db.productsList('electronics')
    print queryFetch
    return render_template("product.html", queryFetch=queryFetch, electronics = True, loginRequired = dict['loginRequired'], name = dict['username'])
    
@app.route('/furniture')
def furniture():
    dict = loginCheck()
    queryFetch = db.productsList('furniture')
    print queryFetch
    return render_template("product.html", queryFetch=queryFetch, furniture = True, loginRequired = dict['loginRequired'], name = dict['username'])
    
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
        session['username_redirect'] = username
        #session['loginRequired'] = False
        passed = True
        name = username
        print(session['loginRequired'])
        


        emit('redirect','/', namespace='/eCom')
        #emit('loginText', name)
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
            emit('redirect','/', namespace='/eCom')

#######################################################Seller Info #################################
@socketio.on('sellerInfo', namespace='/eCom')
def sellerInfo(sellername):
    information = db.getSellerInfo(sellername)
    print information
    emit ('returnSellerInfo',information)
    
################################################Post Product #########################################
@socketio.on('postProduct', namespace='/eCom')
def postProduct(productName,price,quantity,category,desc, today):
    print (productName,price,quantity,category,desc, today)
    session['id'] = uuid.uuid1()
    dict = loginCheck()
    id = str(session['id'])
    db.insertProduct(id,dict['username'],productName,price,quantity,category,desc, today)
    
    emit('redirect','/', namespace='/eCom')
    
    
    
    
# start the server
if __name__ == '__main__':
        socketio.run(app,host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
    