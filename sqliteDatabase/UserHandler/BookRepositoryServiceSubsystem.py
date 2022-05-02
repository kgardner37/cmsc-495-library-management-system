
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .models import Book, Copy, User, returned, barrowed
from User import login
from __main__ import app, db

# flask_login initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
class BookRepositoryServiceSubsystem():

 @app.route('/checkIn/', methods=['GET', 'POST']) 
 def checkIn():
      if request.method == 'GET':
           copyBook = Copy.query.filter_by(issued_by=current_user.id).all()
         if copyBook:!=None:
           db.session.add(returned)
           db.session.delect(barrowed)
            db.session.commit()
             flash('Book returned successfully')
            return redirect(url_for('index.html'))

@app.route('/checkOut/', methods=['GET', 'POST'])
  def checkOut():
      if request.method == 'GET':
          books = Book.query.filter_by(Book.id==request.form['bookId']).first()
          if books!=None:
             books.copy=request.form['copy']
             books.available=request.form['available']
              books.author=request.form['author']
               db.session.commit()
              flash("Book Updated Successfully!")
         else:
            db.session.add(Books(request.form['bookId'],request.form['copy'], request.form['author']))
            db.session.commit()
             flash("Book checkout Successfully!")
          return render_template('index.html')

@app.route('/delectUser/', methods=['GET', 'POST']) 
  def delectUser(user_Id):
	user = User.query.filter_by(user.id=(user_id=user_Id).first()
      if user:
        
          db.session.delete(User(request.form['user_Id'], request.form['name'],request.form['password'],request.form['email']))
            db.session.commit()
                flash(' user delected ')
       else:
           user.username = request.form['name']
            user.password = request.form['password']
             user.email = request.form['email']
              db.session.commit()
             
          flash(' User updated ')
    return redirect(url_for('index.html'))
         
 @app.route('/addUser/', methods=['GET', 'POST']) 
  def addUser(user_Id):
           user = User.query.filter_by(user.id=(user_id=user_Id).first()
      if user:
        
          db.session.add(User(request.form['name'], request.form['name'],request.form['password'],request.form['email']))
            db.session.commit()
                flash(' user added')
       else:
           user.username = request.form['name']
            user.password = request.form['password']
             user.email = request.form['email']
              db.session.commit()
          flash(' User updated ')
    return redirect(url_for('index.html'))

@app.route('/addBook/', methods=['GET', 'POST']) 
  def addBook(bookId):
        if request.method == 'GET':
         bookId = request.form.get("bookId")
         bookName = request.form.get("bookName")
        author = request.form.get("author")
        description = request.form.get("description")
        book = Book.query.filter_by(bookId=bokId).first()
       if book:
         flash(Book Exist!)
         return  redirect(url_for('index.html'))
        db.session.add.(book)
         db.session.commit()
flash('Book Successfully Added!')
return redirect(url_for('index.html'))

@app.route('/DelectBook/', methods=['GET', 'POST'])
def DelectBook(bookId):
         if request.method == 'GET':
         bookId = request.form.get("bookId")
         bookName = request.form.get("bookName")
        author = request.form.get("author")
        description = request.form.get("description")
        book = Book.query.filter_by(bookId=bookId).first()
        if book:
         flash(Book Exist!)
         return  redirect(url_for('index.html'))
        db.session.delect.(book)
         db.session.commit()
flash('Book Successfully Delected!')
return redirect(url_for('index.html'))

@app.route('/upDateBook/', methods=['GET', 'POST'])
def upDateBook():
     if request.method == 'GET':
         bookId = request.form.get("bookId")
         bookName = request.form.get("bookName")
        author = request.form.get("author")
        description = request.form.get("description")
         db.session.update()
         db.session.commit()
         flash("successfully updated")
         return redirect(url_for('index.html'))

