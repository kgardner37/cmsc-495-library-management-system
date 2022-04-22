from __future__ import print_function
from flask import Flask, url_for, flash, request, session, redirect, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret'

# sqlalchemy database initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import sqliteDatabase.UserHandler.UserHandler

@app.route('/')
def index():
    return redirect(url_for('load_home'))
    # ''' This will route the user to the home page.'''
    # if 'username' in session:
    #     return redirect(url_for('load_home'))
    # else:
    #     return render_template('user-login-form.html', title='Login Page')

@app.route('/home/')
def load_home():
        return render_template('index.html', title='Library Management System')

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
