from __future__ import print_function
from flask import Flask, url_for, flash, request, session, redirect, render_template, jsonify, make_response
from datetime import datetime

app = Flask(__name__)

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
    app.run()
