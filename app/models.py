from flask_login import UserMixin
from app import db 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    buckets = db.relationship('Bucket', backref='user', lazy='dynamic')


class Bucket(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    bucketname = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='bucket', lazy='dynamic', cascade="all, delete-orphan")


class Item(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(15), server_default='Not Done')
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'))
