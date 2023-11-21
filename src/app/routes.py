from src.app import app, db, cache
from src.app.models import User
from src.app.forms import SignUpForm, SignInForm
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt, uuid
import os
from datetime import datetime

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signin', methods=['GET', 'POST']) # users/signin is the URL for the sign in page, and the methods are GET and POST
def users_signin(): # this function is called when the user visits the sign in page
    form = SignInForm() # create a sign in form and use SignInForm() from forms.py
    if form.validate_on_submit(): # if the request is a POST
        user = User.query.filter_by(id=form.id.data).first()  # get the user from the database via id
        if not user: # if the user does not exist.
            flash('Could not find user. Try again?')  # flash a message
            return redirect(url_for('index'))
        if not bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd): # Check if the password entered matches the hashed password stored
            flash('Invalid password') # flash a message if it is incorrect.
            return render_template('signin.html', form=form) 
        login_user(user)  # Log in the user
        print(user.email) # Print the user's email
        return redirect(url_for('index')) # redirect to the index page
    return render_template('signin.html', form=form)

@app.route('/users/signup', methods=['GET', 'POST']) # users/signup is the URL for the sign up page, and the methods are GET and POST
def users_signup(): # this function is called when the user visits the sign up page
    form = SignUpForm() # create a sign up form and use SignUpForm() from forms.py
    if form.validate_on_submit(): # if the request is a POST
        existing_user = User.query.filter_by(id=form.id.data).first() # get the user from the database via id
        if existing_user: # if the user exists
            flash('Email already in use') # flash a message
            return render_template('signup.html', form=form) # render the sign up page again
        if form.passwd.data != form.passwd_confirm.data:    # Check if the passwords match
            flash('Passwords do not match') # flash a message if they don't
            return render_template('signup.html', form=form) # render the sign up page again
        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.passwd.data.encode('utf-8'), salt)
        # Create a new user
        new_user = User(
            email=form.email_address.data,
            id = form.id.data,
            passwd=hashed_password,
            # ...possibly other fields ...
        )
        db.session.add(new_user) # add the new user to the database
        try: # try to commit the changes
            db.session.commit() # commit the changes
            flash('Account created successfully!') # flash a message
            return redirect(url_for('beats')) # redirect to the index page
        except Exception as e: # if an exception occurs
            db.session.rollback() # rollback the changes
            # Log the exception 
            print(e)
            flash('An error occurred while creating your account. Please try again.')
    return render_template('signup.html', form=form)

@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user()
    return redirect(url_for('index'))

