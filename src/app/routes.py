from src.app import app, db, cache
from src.app.models import User, Beat, Comment
from src.app.forms import SignUpForm, SignInForm, BeatForm
from flask import render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt, uuid
from werkzeug.utils import secure_filename
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
        return redirect(url_for('beats')) # render the beats page
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
            return redirect(url_for('users_signin')) # redirect to the sign in page
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

@login_required
@app.route('/beats', methods=['GET', 'POST'])
def beats():
    beats = Beat.query.all()
    return render_template('beats.html', beats=beats)

@login_required
@app.route('/beats/new', methods=['GET', 'POST'])
def beats_new():
    form = BeatForm()
    if form.validate_on_submit():
        audio_file = form.audio_file.data
        filename = secure_filename(audio_file.filename)
        audio_file_path = os.path.join('src', 'app', 'uploads', filename)
        audio_file.save(audio_file_path)
        new_beat = Beat(
            id = str(uuid.uuid4()),
            title = str(form.title.data),
            artist = str(current_user.id),
            description = str(form.description.data),
            audio_file = filename,
            date_added = datetime.now()
        )
        
        print(type(new_beat.id))
        print(type(new_beat.title))
        print(type(new_beat.artist))
        print(type(new_beat.description))
        print(type(new_beat.date_added))
        
        db.session.add(new_beat)
        try:
            db.session.commit()
            flash('Beat created successfully!')
            return redirect(url_for('beats'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your beat. Please try again.')
            print(e)
    else:
        print("Form validation failed")
        print(form.errors)
    return render_template('beats_new.html', form=form)

@app.route('/beat/<string:beat_id>')
def beat_detail(beat_id):
    beat = Beat.query.get_or_404(beat_id)
    comments = Comment.query.filter_by(beat_id=beat.id).order_by(Comment.date_posted.desc()).all()
    return render_template('beat_detail.html', beat=beat, comments=comments)


@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory('src/app/uploads', filename)

@app.route('/add-comment/<string:beat_id>', methods=['POST'])
@login_required
def add_comment(beat_id):
    content = request.form.get('content')
    if content:
        comment = Comment(content=content, beat_id=beat_id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.')
    else:
        flash('Comment cannot be empty.')
    return redirect(url_for('beat_detail', beat_id=beat_id))

#route for '/beat_user/<user.id>' page, shows all beats the user in question. if current_user, show delete button.
@login_required
@app.route('/beat_user/<string:user_id>')
def beat_user(user_id):
    beats = Beat.query.filter_by(artist=user_id).all()
    return render_template('beats.html', beats=beats)

@login_required
@app.route('/beat_user/<string:user_id>/delete/<string:beat_id>')
def beat_user_delete(user_id, beat_id):
    beat = Beat.query.get_or_404(beat_id)
    if beat.artist == user_id:
        db.session.delete(beat)
        db.session.commit()
        flash('Beat deleted successfully!')
    else:
        flash('You cannot delete this beat.')
    return redirect(url_for('beat_user', user_id=user_id))

@login_required
@app.route('/my_profile')
def my_profile():
    return render_template('my_profile.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/github')
def github():
    # send user to github page https://github.com/simaomansur/beat-layer in a new tab
    return redirect("https://github.com/simaomansur/beat-layer", code=302)