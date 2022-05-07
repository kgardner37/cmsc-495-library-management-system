from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from app import app, db, login_manager
import sqliteDatabase.UserHandler.UserHandler as uh
import sqliteDatabase.Models.Models as models

@app.route('/payFine/<id>', methods=['GET', 'POST'])
def payFine(id):
    ''' Marks a due fee "paid". '''
    book = models.Book.query.filter(models.Book.id == id).first()
    if request.method == 'POST':
        payer = book.borrower
        amount = book.checkFine()
        date = datetime.now()
        payment = models.Payment(amount=amount, payer=payer, book=book.title, date=date)
        db.session.add(payment)
        book.due = datetime.now() + timedelta(days=7)
        db.session.commit()
        flash('Payment successful!', 'info')
        return redirect(url_for('index'))
    else:
        return render_template('layout.html', template='payment.html', title='Overdue Fee Payment', book=book)