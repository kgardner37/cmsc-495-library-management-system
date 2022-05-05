from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from app import app, db, login_manager
import sqliteDatabase.UserHandler.UserHandler as uh
import sqliteDatabase.Models.Models as models

@app.route('/checkIn/<id>', methods=['GET', 'POST'])
def checkIn(id):
    ''' Checks the book in.
	Sets "borrower" to None and "due" to None. '''
    book = models.Book.query.filter(models.Book.id == id).first()
    book.borrower = None
    book.due = None
    db.session.commit()
    flash('Checked in successfully!', 'info')
    return redirect(url_for('index'))

@app.route('/checkOut/<id>', methods=['GET', 'POST'])
def checkOut(id):
    ''' Checks the book out to the current user.
	Sets "borrower" to user's username and "due" to current date + 7 days. '''
    book = models.Book.query.filter(models.Book.id == id).first()
    book.borrower = current_user.username
    book.due = datetime.now() + timedelta(days=7)
    db.session.commit()
    flash('Checked out successfully!',  'info')
    return redirect(url_for('index'))
    
@app.route('/renew/<id>', methods=['GET', 'POST'])
def renew(id):
    ''' Extends the due date of the book.
	Sets "due" to current due date + 7 days. '''
    book = models.Book.query.filter(models.Book.id == id).first()
    book.due = book.due + timedelta(days=7)
    db.session.commit()
    flash('Renewed successfully!', 'info')
    return redirect(url_for('index'))
