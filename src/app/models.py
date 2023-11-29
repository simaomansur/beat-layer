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

# layers in beat
class Layer(db.Model):
    __tablename__ = 'layers'
    id = db.Column(db.String, primary_key=True)
    beat_id = db.Column(db.String, db.ForeignKey('beats.id'), nullable=False)
    name = Column(String) # name of layer
    created_by = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    date_added = Column(DateTime) # date added to beat bank
    notes = Column(String) # notes about layer
    audio_file = Column(String) # path to audio file
    stems = db.relationship('Stems', backref='layer', lazy=True) # stems/parts in layer

# stems/parts in layer
class Stems(db.Model):
    __tablename__ = 'stems'
    id = db.Column(db.String, primary_key=True)
    layer_id = db.Column(db.String, db.ForeignKey('layers.id'), nullable=False)
    name = Column(String) # name of stem/part
    created_by = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    date_added = Column(DateTime) # date added to beat bank
    notes = Column(String) # notes about stem/part
    audio_file = Column(String) # path to audio file