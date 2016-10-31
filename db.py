import psycopg2
import psycopg2.extras
import os

def db_connect():
    print 'connection to the db_connect'
    connectionString='dbname=ecom user=usman password=usman host=localhost'
    try:
        print 'are we trying'
        return psycopg2.connect(connectionString)
    except:
        print 'cannot connect to the database'
###############################login############################################        
def login(username, password):
    conn=db_connect()
    cur =conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select * from users where username=%s and password=crypt(%s, password);",(username,password))
    loginQueryFetch=cur.fetchone()
    return loginQueryFetch
#############################register###########################################    
def registerIntoDb(username, firstName, lastName, password, conPassword, address, city,state, zip, country, email):
    conn=db_connect()
    cur =conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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

####################################check if username exist ########################
def checkUserNameExist(username):
    conn=db_connect()
    cur =conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Check if username already exists
    query = "SELECT username FROM users WHERE username = %s"
    cur.execute(query, [username])
    userCheck = cur.fetchall()
    return userCheck
    
    
##########################populate cart#############################
def productsList(catagory):
    conn=db_connect()
    cur =conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    query = "SELECT * FROM products WHERE catagory_name = %s"
    cur.execute(query,[catagory])
    userCheck = cur.fetchall()
    return userCheck
    
#############################seller info##################################
def getSellerInfo(sellername):
    conn=db_connect()
    cur =conn.cursor()
    
    query = "SELECT username, firstname, lastname, address, city, state, zip, country, email  FROM users WHERE username = %s"
    cur.execute(query,[sellername])
    sellerInfo = cur.fetchall()
    #print sellerInfo[1]
    for result in sellerInfo:
        temp = {'firstname': result[1], 'lastname': result[2], 'address':result[3], 'city':result[4], 'state':result[5],'zip':result[6],'country':result[7],'email':result[8]}
        
    return temp
    
    