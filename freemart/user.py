from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from . import db

from .models import Product, User, Message


user = Blueprint('user', __name__, url_prefix="/user")


@user.route("/profile", methods=["GET", "POST"])
@user.route("/", methods=["GET", "POST"])
@login_required
def profile_page():
    if request.method == "POST":
        productName = request.form.get('productName')
        product = Product.query.filter_by(name=productName).first()
        seller = User.query.filter_by(id=product.user_id).first()

        if current_user.balance < product.price:
            flash("Purchase error: Insufficient funds", category="error")
        else:
            current_user.balance -= product.price
            seller.balance += product.price

            product.listed = False
            product.user_id = current_user.id

            db.session.commit()
    
    userSelling = [product for product in current_user.posts if product.listed == True]
    userOwned = [product for product in current_user.posts if product.listed == False]
    return render_template("user/profile.html", user=current_user, userSelling=userSelling, userOwned=userOwned)


@user.route('/chatroom')
@login_required
def chatroom_page():
    messages = Message.query.all()
    
    return render_template('user/chatroom.html', user=current_user, messages=messages) 