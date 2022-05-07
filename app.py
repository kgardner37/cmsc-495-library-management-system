from __future__ import print_function
from flask import Flask, url_for, flash, request, session, redirect, render_template, jsonify, make_response
from flask_login import LoginManager, current_user, login_user, UserMixin, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.secret_key = 'secret'

# sqlalchemy database initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# flask_login initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import sqliteDatabase.UserHandler.UserHandler as uh
import sqliteDatabase.BookRepositoryService.BookRepositoryService as brs
import sqliteDatabase.Models.Models as models
import sqliteDatabase.AccountingService.AccountingService as ac

@app.route('/')
def index():
    return redirect(url_for('load_home'))

@app.route('/home/')
@login_required
def load_home():
    query = request.args.get('search')
    if query:
        books = models.Book.query.filter(models.Book.title.contains(query) | models.Book.author.contains(query))
    else:
        books = models.Book.query.all()
    return render_template('layout.html', template='index.html', title='Home', books=books, query=query)


## ADMIN SET-UP ##

# restricts access to data to users with admin role
class AdminView(ModelView):
    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        return current_user.isAdmin
    def inaccessible_callback(self, name, **kwargs):
        flash("Login as administrator to view this page.")
        return redirect(url_for('index'))


class UserView(AdminView):
    can_delete = True
    column_hide_backrefs = False
    column_list = ["id", "username", "password", "isAdmin"]
    column_searchable_list = ["id", "username"]


class BookView(AdminView):
    can_delete = True
    column_hide_backrefs = False
    column_list = ["id", "title", "author", "summary", "borrower", "due"]
    column_searchable_list = ["id", "title", "author", "borrower"]
    
class PaymentView(AdminView):
    can_delete = True
    column_hide_backrefs = False
    column_list = ["id", "payer", "book", "amount", "date"]
    column_searchable_list = ["id", "payer", "book", "date"]


admin = Admin(app, name='Library Management System Administration Page', template_mode='bootstrap3')
admin.add_view(UserView(models.User, db.session))
admin.add_view(BookView(models.Book, db.session))
admin.add_view(PaymentView(models.Payment, db.session))

#################

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
