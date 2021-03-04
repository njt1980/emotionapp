from flask import Flask,render_template,request,session,redirect,url_for
from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
from mongoengine import connect
import mongoengine as me


print(__name__)

app = Flask(__name__);


app.secret_key = "mysecretkey";

app.config['MYSQL_HOST'] = 'localhost';
app.config['MYSQL_USER'] = 'john';
app.config['MYSQL_PASSWORD'] = 'barca4me';
app.config['MYSQL_DB'] = 'myusersdb';

mysql = MySQL(app)
mongoconnect = connect(db="testdb",host="localhost",port=27017)

class newdata(me.Document):
    userid = me.StringField(required=True)
    emotion = me.StringField(required=True)
    reason = me.StringField(required=False)
    #timenow = me.DateTimeField(required=True)

#newentry = newdata(userid="myuserid",emotion="happy1",reason="justlikethat")

#newentry.save()
    

@app.route('/')
@app.route('/login' , methods = ["GET","POST"] )
def login():
    print(request)
    print(request.form)
    msg = ''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form['username'];
        password = request.form['password'];
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor);
        cursor.execute('SELECT * FROM accounts where username=%s and password=%s',(username,password));
        account = cursor.fetchone();
        if account:
            session['loggedin'] = True;
            session['id'] = account['id'];
            session['username'] = account['username'];
            msg = 'Logged in Successfully';
            print("PRINTING..")
            print(session['id'])
            print(session['username'])
            #return render_template('index.html', msg = msg);
            return render_template('enter.html')
        else:
            msg = 'Incorrect username/password';
        

    return(render_template('login.html',msg = msg))

@app.route('/logout')
def logout():
    session.pop('loggedin',None);
    session.pop('id',None);
    session.pop('username',None);
    #return render_template('login.html')
    return redirect(url_for('login'))   

@app.route('/register', methods = ["GET","POST"])
def register():
    msg = '';
    if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username'];
        password = request.form['password'];
        email = request.form['email'];
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor);
        cursor.execute('SELECT * FROM accounts where username=%s',(username,));
        account = cursor.fetchone()
        if account:
            msg = 'User Exists.Please use a different username';
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL,%s,%s,%s)',(username,password,email,));
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html',msg=msg);

@app.route('/howyoufeeling',methods = ["GET","POST"])
def enteremotion():
    now = datetime.now();
    date_time = now.strftime("%A %m/%d/%Y, %H:%M:%S");
    #print(date_time)
    #print(request.method)
    #print(request.form)
    #print(request)
    if request.method == "POST":
        #print(now.timestamp())
        print(request.form['emotion']);
        print(session['username']);
        newentry = newdata(userid = session['username'],emotion = request.form['emotion'],reason="justlikethat");
        print(newentry)
        newentry.save();
        print("Saved")
       
    return render_template('enter.html',date_time=date_time)