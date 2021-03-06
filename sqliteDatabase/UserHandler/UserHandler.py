from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqliteDatabase.BookRepositoryService.BookRepositoryService as brs
import sqliteDatabase.Models.Models as models
from app import app, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    ''' Standard method used by libraries to load a user by id. '''
    return models.User.query.get(int(user_id))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    ''' Creates a new account if the username posted is unique and
        the two passwords posted are matching.
        If successful, account is logged in and redirected to the load_home page.
        If invalid creds are entered, flashes an error. '''
        
    if request.method == 'POST':
    
        username = request.form.get('username')
        password = request.form.get('password')
        verify = request.form.get('verify_password')
        
        if password != verify:
            flash('Mismatching passwords.', 'error')
        else:
            if models.User.query.filter(models.User.username==username).first():
                flash('Username unavailable.', 'error')
            else:
                user = models.User(username=username, password=password, isAdmin=False)
                db.session.add(user)
                db.session.commit()
                
                login_user(user)
                flash('Registration successful.', 'info')
                return redirect(url_for('load_home'))
            
        return render_template('layout.html', template='user-register-form.html', title='Register')
        
    else:
        if current_user.is_authenticated:
            return redirect(url_for('load_home'))
        return render_template('layout.html', template='user-register-form.html', title='Register')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    ''' Logs in the account if a valid username and password are posted.
        If successful, redirects user to the load_home page.
        If invalid creds are entered, flashes an error. '''
        
    if request.method == 'POST':
    
        username = request.form.get('username')
        user = models.User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(request.form.get('password')):
            flash('Invalid credentials.', 'error')
        else:
            login_user(user)
            flash('Login successful.', 'info')
            return redirect(url_for('load_home'))
        return render_template('layout.html', template='user-login-form.html', title='Log In')
    else:
        if current_user.is_authenticated:
            return redirect(url_for('load_home'))
    return render_template('layout.html', template='user-login-form.html', title='Log In')

@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    ''' Logs out the current user.
        Redirects to the login page. '''
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))
