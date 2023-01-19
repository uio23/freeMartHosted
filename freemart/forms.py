from flask_wtf import FlaskForm

from wtforms import  StringField, PasswordField, SubmitField, FileField, TextAreaField, DecimalField, BooleanField, validators, ValidationError

from passlib.hash import pbkdf2_sha256

import requests

import json

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
    self.response = requests.get("https://opentdb.com/api.php?amount=3&category=9&difficulty=medium&type=boolean")
    self.raw = self.response.json()
    self.content = self.raw['results']
    print(self.content)

    qOne = BooleanField("q1_label", validators=[validators.InputRequired(message="Please answer this question")])
    qTwo = BooleanField("q2_label", validators=[validators.InputRequired(message="Please answer this question")])
    qThree = BooleanField("q3_label", validators=[validators.InputRequired(message="Please answer this question")])
    submit_button = SubmitField('Submit')
