# Importing 3rd party components
from flask_wtf import FlaskForm

from sqlalchemy import func

from wtforms import  StringField, PasswordField, SubmitField, FileField, TextAreaField, DecimalField, RadioField, validators, ValidationError, EmailField

from passlib.hash import pbkdf2_sha256

import urllib.parse

import requests

import json

# Importing freemart components
from .models import Product, User

from .helperFunc import isFloat


# ----- Form template definition ----- #

class RegisterForm(FlaskForm):
    username = StringField('username_label', validators=[validators.InputRequired(message="Username required"), validators.Length(min=4, max=12, message="Username must be between 4 and 12 charecters")])
    email = EmailField('email_label', validators=[validators.InputRequired(message="Email required"), validators.Email('Enter valid email')])
    password = PasswordField('password_label', validators=[validators.InputRequired(message="Password required"), validators.Length(min=4, max=24, message="Password must be between 4 and 24 charecters")])
    submit_button = SubmitField('Sign up')

    def validate_username(self, username):
        username = username.data.strip()
        user = User.query.filter(func.lower(User.username)==func.lower(username)).first()

        if user:
            raise ValidationError("Username already exists (case insensitive)")

    def validate_email(self, email):
        email = email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if user:
            raise ValidationError("Account with this email already exists")



def invalid_credentials(form, feild):
    username = form.username.data.strip()
    user = User.query.filter(func.lower(User.username)==func.lower(username)).first()

    if not user:
        raise ValidationError("Incorrect username of password")
    elif not pbkdf2_sha256.verify(form.password.data, user.password):
        raise ValidationError("Incorrect username of password")
class LoginForm(FlaskForm):
    username = StringField("username_label", validators=[validators.InputRequired(message="Username required")])
    password = PasswordField("password_label", validators=[validators.InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Login')



class PostForm(FlaskForm):
    productName = StringField("product_name_label", validators=[validators.InputRequired(message="Product name required"), validators.Length(min=0, max=50, message="Prodcut name too long (50char max)")])
    productDescription = TextAreaField("product_description_label", validators= [validators.Length(min=0, max=140, message="Prodcut description too long (140char max)")])
    productPrice = DecimalField("product_price_label", places=2, validators=[validators.InputRequired(message="Product price required"), validators.NumberRange(min=0.00, message="Price cannot be negative")])
    productImage = FileField("product_image_label", validators=[validators.InputRequired(message="Product image required")])
    submit_button = SubmitField('Post')

    def validate_productName(self, productName):
        productName = productName.data.replace(' ','')

        if not productName.isalpha():
            raise ValidationError("Name must only contain letters")
        product = Product.query.filter(func.lower(Product.name)==func.lower(productName)).first()

        if product:
            raise ValidationError("A product with this name already exists (case insensitive)")

    def validate_productPrice(self, productPrice):
        productPrice = productPrice.data
        if not isFloat(productPrice):
            raise ValidationError("Price must be a number")

    def validate_productImage(self, productImage):
        productImage = productImage.data

        if productImage.filename.split('.')[-1] not in ('jpg', 'png', 'jpeg'):
            raise ValidationError('Only jpg, jpeg or png supported')



class QuizForm(FlaskForm):
    response = requests.get("https://opentdb.com/api.php?amount=3&category=9&difficulty=medium&type=boolean&encode=url3986")
    raw = response.json()
    content = raw['results']
    questions = [[urllib.parse.unquote(content[0]["question"]), content[0]["correct_answer"]], [urllib.parse.unquote(content[1]["question"]), content[1]["correct_answer"]], [urllib.parse.unquote(content[2]["question"]), content[2]["correct_answer"]]]

    qOne = RadioField(questions[0][0], choices=[("True", "True"), ("False", "False")], validators=[validators.InputRequired(message="Please answer this question")])
    qTwo = RadioField(questions[1][0], choices=[("True", "True"), ("False", "False")], validators=[validators.InputRequired(message="Please answer this question")])
    qThree = RadioField(questions[2][0], choices=[("True", "True"), ("False", "False")], validators=[validators.InputRequired(message="Please answer this question")])
    submit_button = SubmitField('Submit')
