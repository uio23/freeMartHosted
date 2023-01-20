from flask_wtf import FlaskForm

from wtforms import  StringField, PasswordField, SubmitField, FileField, TextAreaField, DecimalField, RadioField, validators, ValidationError

from passlib.hash import pbkdf2_sha256

import requests

import json

import urllib.parse

from .models import Product, User


class RegisterForm(FlaskForm):
    username = StringField('username_label', validators=[validators.InputRequired(message="Username required"), validators.Length(min=4, max=12, message="Username must be between 4 and 12 charecters")])
    password = PasswordField('password_label', validators=[validators.InputRequired(message="Password required"), validators.Length(min=4, max=24, message="Password must be between 4 and 24 charecters")])
    confirm_pswd = PasswordField('confirm_pswd_label', validators=[validators.InputRequired(message="Confirm your password"), validators.EqualTo('password', message="Passwords do not match")])
    submit_button = SubmitField('Sign up')

    def validate_username(self, username):
        username = username.data
        user = User.query.filter_by(username=username).first()

        if user:
            raise ValidationError("Username already exists")


def invalid_credentials(form, feild):
    username = form.username.data
    user = User.query.filter_by(username=username).first()

    if not user:
        raise ValidationError("Incorrect username of password")
    elif not pbkdf2_sha256.verify(form.password.data, user.password):
        raise ValidationError("Incorrect username of password")

class LoginForm(FlaskForm):
    username = StringField("username_label", validators=[validators.InputRequired(message="Username required")])
    password = PasswordField("password_label", validators=[validators.InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Login')


class ListingForm(FlaskForm):
    productName = StringField("product_name_label", validators=[validators.InputRequired(message="Product name required")])
    productDescription = TextAreaField("product_description_label", validators= [validators.Length(min=0, max=250, message="Prodcut description too long (250char max)")])
    productPrice = DecimalField("product_price_label", places=2, validators=[validators.InputRequired(message="Product price must be a number"), validators.NumberRange(min=0.00, message="Price cannot be negative")])
    productImage = FileField("product_image_label", validators=[validators.InputRequired(message="Product image required")])
    submit_button = SubmitField('Post')

    def validate_productName(self, productName):
        productName = productName.data
        product = Product.query.filter_by(name=productName).first()

        if not productName.replace(' ','').isalpha():
            raise ValidationError("Name must only contain letters")
        elif product:
            raise ValidationError("A product with this name already exists")

    def validate_productImage(self, productImage):
        productImage = productImage.data

        if productImage.filename.split('.')[-1] not in ('jpg', 'png', 'jpeg'):
            raise ValidationError("Wrong file-type")


def validate_resell(productName, newPrice, user):
    product = Product.query.filter_by(name=productName).first()

    if product.username == user.username:
        try:
            newPrice = round(float(newPrice), 2)
            if newPrice > 0.0:
                newProduct = Product(name=productName, description=product.description, price=newPrice, listed=True, imagePath=product.imagePath, username=user.username)
                return True, newProduct

            else:
                return False, "Re-sell failed: Price cannot be negative"

        except ValueError:
            return False, "Re-sell failed: Please specify a valid price decimal"

    else:
        return False, "Re-sell failed: You are not the owner of this item"


class QuizForm(FlaskForm):
    response = requests.get("https://opentdb.com/api.php?amount=3&category=9&difficulty=medium&type=boolean&encode=url3986")
    raw = response.json()
    content = raw['results']
    questions = [[urllib.parse.unquote(content[0]["question"]), content[0]["correct_answer"]], [urllib.parse.unquote(content[1]["question"]), content[1]["correct_answer"]], [urllib.parse.unquote(content[2]["question"]), content[2]["correct_answer"]]]


    qOne = RadioField(questions[0][0], choices=[("True", "True"), ("False", "False")], validators=[validators.InputRequired(message="Please answer this question")])
    qTwo = RadioField(questions[1][0], choices=[("True", "True"), ("False", "False")], validators=[validators.InputRequired(message="Please answer this question")])
    qThree = RadioField(questions[2][0], choices=[("True", "True"), ("False", "False")], validators=[validators.InputRequired(message="Please answer this question")])
    submit_button = SubmitField('Submit')

    def validate_qOne(self, qOne):
        q1 = qOne.data

        if questions[0][-1] != str(q1):
            raise ValidationError("Wrong")

    def validate_qTwo(self, qTwo):
        q2 = qTwo.data

        if questions[1][-1] != str(q2):
            raise ValidationError("Wrong")

    def validate_qThree(self, qThree):
        q3 = qThree.data

        if questions[2][-1] != str(q3):
            raise ValidationError("Wrong")
