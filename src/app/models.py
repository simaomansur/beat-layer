# -----------------------------------------------------------
# Project: BeatBank
# File: models.py
# Description: This file contains the models for the app. It is
# imported by the __init__.py file in the same directory.
#
# Author: Parker Tonra, Simao Mansur
# -----------------------------------------------------------

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from src.app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True)
    passwd = db.Column(db.LargeBinary)
    beats = db.relationship('Beat',
                            backref='creator',
                            lazy='dynamic'
                            )
    comments = db.relationship('Comment',
                               back_populates='author',
                               lazy='dynamic'
                               )
    likes = db.relationship('Like', backref='user', lazy='dynamic')
    profile_pic = db.Column(
        db.String, default='pictures/profile_pictures/default_profile_pic.jpg'
        )
    bio = db.Column(db.String, default='This user has not set a bio yet.')


class Beat(db.Model):
    __tablename__ = 'beats'
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    description = db.Column(db.String(100))
    artist = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    audio_file = Column(String)
    genre = db.Column(db.String(32))
    likes = db.relationship('Like', backref='beat', lazy='dynamic')
    comments = db.relationship('Comment', backref='beat', lazy=True)

    def like_count(self):
        return self.likes.count()


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    beat_id = db.Column(db.String(36),
                        db.ForeignKey('beats.id'),
                        nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', back_populates='comments')


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'))
    beat_id = db.Column(db.String(36), db.ForeignKey('beats.id'))
