from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from app import app, db, login_manager
import sqliteDatabase.UserHandler.UserHandler as uh
import sqliteDatabase.Models.Models as models

@app.route('/checkFine/<id>', methods=['GET', 'POST'])
def checkFine(id):
    ''' Checks amount due on a book. '''
    book = models.Book.query.filter(models.Book.id == id).first()
    amountPaid = 0
    for payment in book.payments:
        amountPaid += payment.amount
    delta = datetime.now() - book.due
    return ((delta.days // 7) * 5) - amountPaid # $5 per week after the due date

@app.route('/payFine/<id>', methods=['GET', 'POST'])
def payFine(id):
    ''' Marks a due fee "paid". '''
    book = models.Book.query.filter(models.Book.id == id).first()
    payer = book.borrower
    amount = checkFine(id)
    date = datetime.now()
    payment = models.Payment(amount=amount, payer=payer, book=book.title, date=date)
    db.session.add(payment)
    db.session.commit()
    flash('Payment successful!', 'info')
    return redirect(url_for('index'))