from flask_login import UserMixin

from . import db


class Product(db.Model):

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(asdecimal=True), nullable=False)
    listed = db.Column(db.Boolean, default=True)
    imagePath = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.name} is an item with the index of {self.id}, selling/sold a price of {self.price}. Listed: {self.listed}.'


class User(db.Model, UserMixin):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float(asdecimal=True), default=500.00)
    posts = db.relationship('Product')
    messages = db.relationship('Message')

    def __repr__(self):
        return f'{self.username} is a user with the id of {self.id}. Their balance is {self.balance}. Posts: {self.posts}. Messages: {self.messages}.'


class Message(db.Model):

    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String, nullable=False)
    username =  db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'ID:{self.id}, Content:{self.msg}, Author:{self.username}.'
