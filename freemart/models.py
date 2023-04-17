from flask_login import UserMixin
from sqlalchemy.sql import func

from datetime import datetime, timedelta

from . import db


class Product(db.Model):

    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(asdecimal=True), nullable=False)
    listed = db.Column(db.Boolean, default=True)
    imagePath = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'))

    def __repr__(self):
        return f'{self.name} is an item with the id of {self.id}, selling/sold at a price of {self.price}. Listed: {self.listed}.'


class User(db.Model, UserMixin):

    __tablename__ = "user"
    yesterdayUTC = datetime.utcnow() - timedelta(days=1)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float(asdecimal=True), default=0.00)
    fmt_balance = db.Column(db.Float(asdecimal=True), default=0.5)
    posts = db.relationship('Product')
    messages = db.relationship('Message')
    lastquiz = db.Column(db.String, nullable=False, default=yesterdayUTC)
    sale_count = db.Column(db.Integer, nullable=False, default=0)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'{self.username} is a user with the id of {self.id}. Their balance is {self.balance}. Posts: {self.posts}. Messages: {self.messages}.'


class Message(db.Model):

    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String, nullable=False)
    username =  db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'ID:{self.id}, Content:{self.msg}, Author:{self.username}.'
