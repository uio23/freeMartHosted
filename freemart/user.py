from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from . import db

from .imageFunc import loadImg

from .models import Product, User, Message


user = Blueprint('user', __name__, url_prefix="/user")


@user.route("/profile/<username>", methods=["GET", "POST"])
@user.route("/<username>", methods=["GET", "POST"])
@login_required
def profile_page(username):
    if request.method == "POST":
        productName = request.form.get('productName')
        product = Product.query.filter_by(name=productName).first()
        seller = User.query.filter_by(username=product.username).first()

        if current_user.balance < product.price:
            flash("Purchase failed: Insufficient funds", category="error")
        else:
            current_user.balance -= product.price
            seller.balance += product.price

            product.listed = False
            product.username = current_user.username

            db.session.commit()

    user = User.query.filter_by(username=username).first()

    userSelling = [product for product in user.posts if product.listed == True]
    for product in userSelling:
        loadImg(product.imagePath)

    userOwned = [product for product in user.posts if product.listed == False]
    for product in userOwned:
        loadImg(product.imagePath)

    return render_template("user/profile.html", user=user, userSelling=userSelling, userOwned=userOwned)


@user.route('/chatroom')
@login_required
def chatroom_page():
    messages = Message.query.all()

    return render_template('user/chatroom.html', user=current_user, messages=messages)
