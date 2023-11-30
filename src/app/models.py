from datetime import datetime

from sqlalchemy import String, Float, Column, DateTime
from src.app import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True)
    passwd = db.Column(db.LargeBinary)
    beats = db.relationship('Beat', backref='creator', lazy='dynamic')

# beats in beat bank
class Beat(db.Model):
    __tablename__ = 'beats'
    id = db.Column(db.String(36), primary_key=True)  # UUIDs are 36 characters long
    title = db.Column(db.String(32), nullable=False)
    date_added = Column(DateTime) # date added to beat bank
    description = db.Column(db.String(100))
    artist = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    audio_file = Column(String) # path to audio file

# comment for specific beat
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    beat_id = db.Column(db.String(36), db.ForeignKey('beats.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)  # Assuming users have an 'id' field

    # Relationships
    beat = db.relationship('Beat', backref=db.backref('comments', lazy=True))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))