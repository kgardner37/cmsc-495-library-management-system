from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db
import sqliteDatabase.AccountingService.AccountingService as ac

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    isAdmin = db.Column(db.Boolean)
    books = db.relationship('Book')
    payments = db.relationship('Payment')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<User id: {self.id}, username: {self.username}, admin: {self.isAdmin}>'

    def check_password(self, password):
        return self.password == password


# Book sqlalchemy model
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    summary = db.Column(db.Text)
    borrower = db.Column(db.String, db.ForeignKey('user.username'), nullable=True)
    due = db.Column(db.DateTime, nullable=True)
    users = db.relationship('User')
    payments = db.relationship('Payment')

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Book id: {self.id}, title: {self.title}, author: {self.author}>'
        
    def isOverdue(self):
        if self.due:
            return datetime.now() > self.due
        return False
    
    def checkFine(self):
        ''' Checks amount due on a book. '''
        totalPaid = 0
        amountsPaid = Payment.query.filter(Payment.book == self.title and Payment.payer == self.borrower and Payment.date > self.due)
        for payment in amountsPaid:
            totalPaid += payment.amount
        delta = datetime.now() - self.due
        return ((delta.days // 7) * 5) - totalPaid # $5 per week after the due date


class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    payer = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    book = db.Column(db.String, db.ForeignKey('book.title'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Payment id: {self.id}, amount: {self.amount}, payer: {self.payer}, book: {self.book}>'

