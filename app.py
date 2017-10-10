from flask import Flask, render_template, flash, redirect, url_for, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask import request
from flask_sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from flask.ext.login import login_user , logout_user , current_user , login_required
from wtforms.fields.html5 import EmailField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__name__)), 'database.db')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

class SearchForm(Form):
	search = StringField(" ", [validators.Length(min=4, max=30)], render_kw={'placeholder':'Search'})

class LoginForm(Form):
	username = StringField(" ", [validators.Length(min=5, max=10)], render_kw={'placeholder':'Username'})
	password = PasswordField(" ", [validators.Length(min=5, max=10)], render_kw={'placeholder':'Password'})
	email = EmailField(" ", [validators.DataRequired(), validators.Email()], render_kw={'placeholder':'email'})
class RegisterForm(Form):
	name = StringField("Name", [validators.Length(min=2, max=20)], render_kw={'placeholder'':Name'})
	email = EmailField("Email", [validators.Length(min=6, max=20)], render_kw={'placeholder':'Email'})
	username = StringField(" ", [validators.Length(min=5, max=10)], render_kw={'placeholder':'Username'})
	password = PasswordField("Password", [validators.Length(min=5)], render_kw={'placeholder':'Password'})
	confirmPw = PasswordField("Confirm Password", [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
		])
@app.route('/', methods=['GET'])
def home():
	form = SearchForm(request.form)
	return render_template('home.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		form = LoginForm(request.form)
		return render_template('login.html', form=form)
	else:
		username = request.form['username']
		password = request.form['password']
		registered_user = User.query.filter_by(username=username,password=password).first()
		if registered_user is None:
		    return redirect(url_for('login'))
		login_user(registered_user)
		return redirect(request.args.get('next') or url_for('index'))
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		form = RegisterForm(request.form)
		return render_template('register.html', form = form)
	else:
		name = request.form['name']
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		confirmPw = request.form['confirmPw']
		return render_template('home.html')
if __name__ == "__main__":
	app.run(debug=True)