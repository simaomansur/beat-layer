# -----------------------------------------------------------
# Project: BeatBank
# File: forms.py
# Description: This file contains the forms for the app. It is
# imported by the __init__.py file in the same directory.
#
# Author: Parker Tonra, Simao Mansur
# -----------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, TextAreaField,
    DateField, SubmitField, FileField, EmailField, SelectField
    )
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import EqualTo


class SignUpForm(FlaskForm):
    id = StringField('Username', validators=[DataRequired()])
    email_address = StringField('Email')
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password',
                                   validators=[DataRequired()])
    submit = SubmitField('Create Account')


class HomeForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class BeatForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    # dropdown for genre
    genre = SelectField(
        'Genre',
        choices=[
            ('rock', 'Rock'),
            ('electronic', 'Electronic'),
            ('jazz', 'Jazz'),
            ('pop', 'Pop'),
            ('hip-hop', 'Hip-Hop'),
            ('country', 'Country'),
            ('r&b', 'R&B'),
            ('classical', 'Classical'),
            ('metal', 'Metal'),
            ('blues', 'Blues'),
            ('folk', 'Folk'),
            ('reggae', 'Reggae'),
            ('latin', 'Latin'),
            ('indie', 'Indie'),
            ('soul', 'Soul')
        ]
    )
    description = TextAreaField('Description', validators=[DataRequired()])
    audio_file = FileField('Audio File',
                           validators=[FileRequired(),
                                       FileAllowed(['mp3', 'wav'],
                                                   'Audio only!')]
                           )
    submit = SubmitField('Create Beat')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Passwords must match.')
    ])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired()])
    submit = SubmitField('Reset Password')
    email = EmailField('Email')


class MyProfileForm(FlaskForm):
    bio = TextAreaField('Bio', default='')
    profile_pic = FileField('Profile Picture',
                            validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                                    'Images only!')]
                            )
    submit = SubmitField('Update Profile')
