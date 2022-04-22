from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __main__ import app, db

# flask_login initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User sqlalchemy model
class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	password = db.Column(db.String)
	isAdmin = db.Column(db.Boolean)

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)

	def __repr__(self):
		return f'<User id: {self.id}, username: {self.username}, admin: {self.isAdmin}>'

	def check_password(self, password):
		return self.password == password

@login_manager.user_loader
def load_user(user_id):
	''' Standard method used by libraries to load a user by id. '''
	return User.query.get(int(user_id))

@app.route('/register/', methods=['GET', 'POST'])
def register():
	''' Creates a new account if the username posted is unique and
		the two passwords posted are matching.
		If successful, account is logged in and redirected to the load_home page.
		If invalid creds are entered, flashes an error. '''
		
	if request.method == 'POST':
	
		error = None
		username = request.form.get('username')
		password = request.form.get('password')
		verify = request.form.get('verify_password')
		
		if password != verify:
			error = 'Mismatching passwords.'
		else:
			user = User(username=username, password=password)
			db.session.add(user)
			db.session.commit()
			
			login_user(user)
			flash('Registration successful.')
			return redirect(url_for('load_home'))
			
		return render_template('user-register-form.html', error=error)
		
	else:
		if current_user.is_authenticated:
			return redirect(url_for('load_home'))
		return render_template('user-register-form.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
	''' Logs in the account if a valid username and password are posted.
		If successful, redirects user to the load_home page.
		If invalid creds are entered, flashes an error. '''
		
	if request.method == 'POST':
	
		error = None
		username = request.form.get('username')
		user = User.query.filter_by(username=username).first()
		
		if user is None or not user.check_password(request.form.get('password')):
			error = 'Invalid credentials.'
		else:
			login_user(user)
			flash('Login successful.')
			return redirect(url_for('load_home'))
		return render_template('user-registration-form.html', error=error)
	else:
		if current_user.is_authenticated:
			return redirect(url_for('load_home'))
	return render_template('user-login-form.html')

@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
	''' Logs out the current user.
		Redirects to the login page. '''
	logout_user()
	flash('Logged out.')
	return redirect(url_for('login'))
