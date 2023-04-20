# Importing 3rd party components
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user

from decimal import Decimal

import re

import math

import random

# Importing freemart component
from . import db

from .imageFunc import loadImgs

from .models import Product, User, Message

from .bonusFunc import calcSaleBonus

from .helperFunc import isFloat, confirmed_required


# User branch blueprint definition
user = Blueprint('user', __name__, url_prefix="/user")


# ----- Routes definition ----- #

@user.route("/profile/<username>", methods=["GET", "POST"])
@user.route("/<username>", methods=["GET", "POST"])
@login_required
@confirmed_required
def profile_page(username):
    '''
        THIS, this, is *the* route

    '''

    user = User.query.filter_by(username=username).first()
    saleBonus = calcSaleBonus(user)
    postedItem = None

    if request.method == "POST":
        productName = request.form.get("productName")
        product = Product.query.filter_by(name=productName).first()
        modalType = request.form.get("modalType")

        if modalType == "purchaseProduct":

            if (current_user.balance < product.price):
                flash("Not enough FMC", category="error")
            elif (current_user.username == product.username):
                flash("You cannot buy from yourself", category="error")
            else:
                seller = User.query.filter_by(username=product.username).first()
                sellerBonus = calcSaleBonus(seller)

                current_user.balance -= product.price
                seller.balance += product.price

                if product.price > int(sellerBonus/4):
                    seller.balance += sellerBonus
                    seller.sale_count += 1

                product.listed = False
                product.username = current_user.username
                postedItem = product

                db.session.commit()
        elif product.username == current_user.username:
            newProductPrice = request.form.get("newProductPrice")

            if newProductPrice:
                # Ignore those try-hards who write out ...FMC in their input, smh
                insensitive_fmc = re.compile(re.escape('fmc'), re.IGNORECASE)
                newProductPrice = insensitive_fmc.sub('', newProductPrice)

                try:
                    newProductPrice = math.floor(float(newProductPrice) * 10 ** 2) / 10 ** 2
                except TypeError:
                    pass

            if modalType == "editProductPrice":
                if not isFloat(newProductPrice):
                    flash("Price must be a number", category="error")
                elif newProductPrice < 0:
                    flash("Cannot set negative price", category="error")
                else:
                    product.price = newProductPrice
                    db.session.commit()
            elif modalType == "removeProduct":
                product.listed = False
                db.session.commit()
                postedItem = product
            elif modalType == "resellProduct":
                if not isFloat(newProductPrice):
                    flash("Price must be a number", category="error")
                elif newProductPrice < 0:
                    flash("Cannot set negative price", category="error")
                else:
                    product.listed = True
                    product.price = newProductPrice
                    db.session.commit()
                    return redirect(url_for('market.market_page', product=product.name))
        else:
            flash("You do not own the product!", category="error")


    loadImgs(user.posts)

    # SELLING
    userSelling = [product for product in user.posts if product.listed == True]
    random.shuffle(userSelling)
    groupedUserSelling = []

    for i in range(0, len(userSelling), 6):
        groupedUserSelling.append(userSelling[i:i+6])

    # OWNEW
    userOwned = [product for product in user.posts if product.listed == False]
    random.shuffle(userOwned)

    if postedItem:
        userOwned.insert(0, userOwned.pop(userOwned.index(postedItem)))
    groupedUserOwned = []

    for i in range(0, len(userOwned), 6):
        groupedUserOwned.append(userOwned[i:i+6])


    return render_template("user/profile.html", user=user, userSelling=groupedUserSelling, userOwned=groupedUserOwned, userOwnedLen=len(userOwned), userSellingLen=len(userSelling), saleBonus=saleBonus, current_user=current_user)


@user.route('/chatroom')
@login_required
@confirmed_required
def chatroom_page():
    '''
        Render chatroom with messages.
    '''

    messages = Message.query.all()

    return render_template('user/chatroom.html', user=current_user, messages=messages)
