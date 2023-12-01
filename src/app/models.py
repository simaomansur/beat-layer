from datetime import datetime
from sqlalchemy import Column, String, DateTime
from src.app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True)
    passwd = db.Column(db.LargeBinary)
    beats = db.relationship('Beat', backref='creator', lazy='dynamic')
    comments = db.relationship('Comment', back_populates='author', lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')

class Beat(db.Model):
    __tablename__ = 'beats'
    id = db.Column(db.String(36), primary_key=True)  # UUIDs are 36 characters long
    title = db.Column(db.String(32), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)  # Date added to beat bank
    description = db.Column(db.String(100))
    artist = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    audio_file = Column(String)  # Path to audio file
    genre = db.Column(db.String(32))
    likes = db.relationship('Like', backref='beat', lazy='dynamic')
    comments = db.relationship('Comment', backref='beat', lazy=True)

    def like_count(self):
        return self.likes.count()

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    beat_id = db.Column(db.String(36), db.ForeignKey('beats.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', back_populates='comments')

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'))  # Match the data type in User model
    beat_id = db.Column(db.String(36), db.ForeignKey('beats.id'))  # Match the data type and name in Beat model
