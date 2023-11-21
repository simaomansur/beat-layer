import datetime

from sqlalchemy import String, Float, Date, Column
from src.app import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True)
    passwd = db.Column(db.LargeBinary)

# beats in beat bank
class Beat(db.Model):
    __tablename__ = 'beats'
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String) # name of beat
    created_by = Column(String) # user id
    bpm = Column(Float) # tempo
    length = Column(String) # length of beat
    key = Column(String) # key of beat
    date_added = Column(Date) # date added to beat bank
    notes = Column(String) # notes about beat
    audio_file = Column(String) # path to audio file
    layers = db.relationship('Layer', backref='beat', lazy=True) # layers in beat

# layers in beat
class Layer(db.Model):
    __tablename__ = 'layers'
    id = db.Column(db.String, primary_key=True)
    beat_id = db.Column(db.String, db.ForeignKey('beats.id'), nullable=False)
    name = Column(String) # name of layer
    created_by = Column(String) # user id
    date_added = Column(Date) # date added to beat bank
    notes = Column(String) # notes about layer
    audio_file = Column(String) # path to audio file
    stems = db.relationship('Stems', backref='layer', lazy=True) # stems/parts in layer

# stems/parts in layer
class Stems(db.Model):
    __tablename__ = 'stems'
    id = db.Column(db.String, primary_key=True)
    layer_id = db.Column(db.String, db.ForeignKey('layers.id'), nullable=False)
    name = Column(String) # name of stem/part
    created_by = Column(String) # user id
    date_added = Column(Date) # date added to beat bank
    notes = Column(String) # notes about stem/part
    audio_file = Column(String) # path to audio file