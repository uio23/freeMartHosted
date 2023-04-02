from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from . import db

from .imageFunc import loadImgs

from .models import Product, User, Message


user = Blueprint('user', __name__, url_prefix="/user")

def not_float(variable):
    try:
        float(variable)
        return False
    except:
        return True

@user.route("/profile/<username>", methods=["GET", "POST"])
@user.route("/<username>", methods=["GET", "POST"])
@login_required
def profile_page(username):
    if request.method == "POST":
        modalType = request.form.get("modalType")
        productName = request.form.get("productName")
        newProductPrice = request.form.get("newProductPrice")

        if not_float(newProductPrice):
            flash("Price must be a number", category="error")
        elif round(float(newProductPrice), 2) < 0:
            flash("Cannot set negative price", category="error")
        elif modalType == "editProductPrice":
            newProductPrice = round(float(newProductPrice), 2)
            product = Product.query.filter_by(name=productName).first()
            product.price = newProductPrice
            db.session.commit()
        elif modalType == "removeProduct":
            product = Product.query.filter_by(name=productName).first()
            product.listed = False
            db.session.commit()
        elif modalType == "resellProduct":
            newProductPrice = round((newProductPrice), 2)
            product = Product.query.filter_by(name=productName).first()
            product.listed = True
            product.price = newProductPrice
            db.session.commit()
        elif modalType == "purchaseProduct":
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

    loadImgs(user.posts)

    userSelling = [product for product in user.posts if product.listed == True]
    groupedUserSelling = []

    for i in range(0, len(userSelling), 6):
        groupedUserSelling.append(userSelling[i:i+6])
    singleSelling = False
    if len(userSelling) == 1:
        singleSelling = True

    userOwned = [product for product in user.posts if product.listed == False]
    groupedUserOwned = []

    for i in range(0, len(userOwned), 6):
        groupedUserOwned.append(userOwned[i:i+6])
    singleOwned = False
    if len(userOwned) == 1:
        singleOwned = True


    return render_template("user/profile.html", user=user, userSelling=groupedUserSelling, userOwned=groupedUserOwned, singleOwned=singleOwned, singleSelling=singleSelling, userOwnedLen=len(userOwned), userSellingLen=len(userSelling), current_user=current_user)


@user.route('/chatroom')
@login_required
def chatroom_page():
    messages = Message.query.all()

    return render_template('user/chatroom.html', user=current_user, messages=messages)
