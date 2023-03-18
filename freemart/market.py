from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

import os

from . import db

from .models import Product

from .forms import ListingForm, validate_resell

from .imageFunc import saveImg, loadImg


market = Blueprint('market', __name__, url_prefix="/market")


@market.route("/post", methods=["GET", "POST"])
@login_required
def post_page():
    listing_form = ListingForm()

    if listing_form.validate_on_submit():
        productName = listing_form.productName.data
        productDescription = listing_form.productDescription.data
        productPrice = round(float(listing_form.productPrice.data), 2)
        productImage = listing_form.productImage.data
        imageFilename = secure_filename(f'{productName.replace(" ", "-")}.{productImage.filename.split(".")[-1]}')

        if saveImg(productImage, imageFilename):
            pass
        else:
            flash("Failed to upload image")
            return render_template("market/post.html", user=current_user, form=listing_form)

        item = Product(name=productName, description=productDescription, price=productPrice, imagePath=imageFilename, username=current_user.username)
        db.session.add(item)
        db.session.commit()

        return redirect(url_for('market.market_page'))

    return render_template("market/post.html", user=current_user, form=listing_form)


@market.route("/market", methods=["GET", "POST"])
@market.route("/", methods=["GET", "POST"])
@login_required
def market_page():
    if request.method == "POST":
        productName = request.form.get("productName")
        newPrice = request.form.get("newPrice")
        valid, outcome = validate_resell(productName, newPrice, current_user)

        if valid:
            product = Product.query.filter_by(name=productName).first()
            db.session.delete(product)
            db.session.commit()

            db.session.add(outcome)
            db.session.commit()
        else:
            flash(outcome, category="error")
            return redirect(url_for('user.profile_page', username=current_user.username))


    items = Product.query.filter_by(listed=True).all()
    groupedItems = []

    for i in range(0, len(items), 6):
        groupedItems.append(items[i:i+6])

    return render_template("market/market.html", user=current_user, items=groupedItems)
