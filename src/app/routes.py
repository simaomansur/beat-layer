# -----------------------------------------------------------
# Project: BeatBank
# File: routes.py
# Description: This file contains the routes for the app. It is
# imported by the __init__.py file in the same directory.
#
# Author: Parker Tonra, Simao Mansur
# -----------------------------------------------------------

from src.app import app, db, mail
from src.app.models import User, Beat, Comment, Like
from src.app.forms import SignUpForm, BeatForm, ForgotPasswordForm, ResetPasswordForm, HomeForm, MyProfileForm
from flask import render_template, redirect, url_for, request, flash, send_from_directory, jsonify
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt, uuid
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('beats'))
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    form = HomeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if not user:
            flash('Could not find user. Try again?')
            return redirect(url_for('index'))
        if not bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            flash('Invalid password')
            return render_template('home.html', form=form) 
        login_user(user)
        return redirect(url_for('beats'))
    return render_template('home.html', form=form)

@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(id=form.id.data).first()
        if existing_user:
            flash('Email already in use')
            return render_template('signup.html', form=form)
        if form.passwd.data != form.passwd_confirm.data:
            flash('Passwords do not match')
            return render_template('signup.html', form=form)
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.passwd.data.encode('utf-8'), salt)
        new_user = User(
            email=form.email_address.data,
            id = form.id.data,
            passwd=hashed_password,
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('Account created successfully!')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            print(e)
            flash('An error occurred while creating your account. Please try again.')
    return render_template('signup.html', form=form)

@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/beats', methods=['GET'])
def beats():
    if not current_user.is_authenticated:
        flash('You must be logged in to view this page.')
        return redirect(url_for('home'))
    genre = request.args.get('genre')
    if genre:
        beat_tuples = Beat.query.filter_by(genre=genre).join(User, User.id == Beat.artist).add_columns(User.profile_pic).all()
    else:
        beat_tuples = Beat.query.join(User, User.id == Beat.artist).add_columns(User.profile_pic).all()
    beats_with_pics = [{'beat': beat, 'profile_pic': profile_pic} for beat, profile_pic in beat_tuples]
    return render_template('beats.html', beats=beats_with_pics)

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
            genre = str(form.genre.data),
            artist = str(current_user.id),
            description = str(form.description.data),
            audio_file = filename,
            date_added = datetime.now()
        )
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
    user = User.query.filter_by(id=beat.artist).first()
    return render_template('beat_detail.html', beat=beat, comments=comments, user=user)

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

@app.route('/beat_user/<string:user_id>')
@login_required
def beat_user(user_id):
    beat_tuples = Beat.query.filter_by(artist=user_id).join(User, User.id == Beat.artist).add_columns(User.profile_pic).all()
    beats_with_pics = [{'beat': beat, 'profile_pic': profile_pic} for beat, profile_pic in beat_tuples]
    return render_template('beats.html', beats=beats_with_pics, user=User.query.get(user_id))

@login_required
@app.route('/beat_user/<string:user_id>/delete/<string:beat_id>', methods=['POST'])
def beat_user_delete(user_id, beat_id):
    beat = Beat.query.get_or_404(beat_id)
    if beat.artist == user_id:
        Comment.query.filter_by(beat_id=beat.id).delete()
        db.session.delete(beat)
        db.session.commit()
        flash('Beat and associated comments deleted successfully!')
    else:
        flash('You cannot delete this beat.')
    return redirect(url_for('beat_user', user_id=user_id))

@login_required
@app.route('/my_profile', methods=['GET', 'POST'])
def my_profile():
    form = MyProfileForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            new_profile_pic = form.profile_pic.data
            filename = secure_filename(new_profile_pic.filename)
            filepath = os.path.join(app.root_path, 'src', 'static', 'pictures', 'profile_pictures', filename)
            print("Saving file to: ", filepath)
            new_profile_pic.save(filepath)
            current_user.profile_pic = os.path.join('pictures', 'profile_pictures', filename)
        current_user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('my_profile'))
    form.bio.data = current_user.bio
    return render_template('my_profile.html', form=form, user=current_user)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/github')
def github():
    return redirect("https://github.com/simaomansur/beat-layer", code=302)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user.email)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('index'))
        else:
            flash('Invalid email address!', 'error')
    return render_template('forgot_password.html', form=form)

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        print("token: ", token)
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = serializer.loads(
            token,
            salt = app.config['SECURITY_PASSWORD_SALT'],
            max_age=3600
        )
        print("email: ", email)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('login'))
    form = ResetPasswordForm()
    if request.method == 'POST':
        print("request method is POST")
        print(form.errors)
    if not form.validate_on_submit():
        print("form not validated")
        print(form.errors)
        return render_template('reset_password.html', form=form, token=token)
    if form.validate_on_submit():
        (print("attempting to change password..."))
        print('email: ', email)
        user = User.query.filter_by(email=email).first()
        print('user: ', user)
        if user:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
            user.passwd = hashed_password
            db.session.commit()
            print("password changed")
            flash('Your password has been updated!', 'success')
            print(form.errors)
            return redirect(url_for('home'))
        else:
            print("user not found")
            flash('Unable to reset password. Your reset link may have expired.', 'error')
    return render_template('reset_password.html', form=form, token=token)

def commit_new_password(token, password):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    email = serializer.loads(
        token,
        salt = app.config['SECURITY_PASSWORD_SALT'],
        max_age=3600
    )
    user = User.query.filter_by(email=email).first()
    if user:
        print("user found, resetting password...")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), email.salt)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    else:
        flash('Unable to reset password. Your reset link may have expired.', 'error')

def send_password_reset_email(user_email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token = serializer.dumps(user_email, salt=app.config['SECURITY_PASSWORD_SALT'])
    user_id = User.query.filter_by(email=user_email).first().id
    reset_url = url_for('reset_with_token', token=token, _external=True)
    email = Message("Password Reset Requested", sender='your@domain.com', recipients=[user_email])
    email.body = f'Username: {user_id}\n\nTo reset your password, visit the following link:\n{reset_url}\n\nIf you did not make this request then simply ignore this email and no changes will be made.'
    mail.send(email)
    
@app.route('/like/<beat_id>', methods=['POST'])
@login_required
def like_song(beat_id):
    existing_like = Like.query.filter_by(user_id=current_user.id, beat_id=beat_id).first()
    if existing_like:
        return jsonify({"success": False, "error": "Already liked"}), 400
    new_like = Like(user_id=current_user.id, beat_id=beat_id)
    db.session.add(new_like)
    db.session.commit()
    return jsonify({"success": True, "likes": Like.query.filter_by(beat_id=beat_id).count()})

@app.context_processor
def utility_processor():
    def get_user(user_id):
        return User.query.get(user_id)
    return dict(get_user=get_user)