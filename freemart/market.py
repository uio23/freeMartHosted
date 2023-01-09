from flask import Blueprint, redirect, render_template, flash, url_for, current_app, request
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

import github

import os

from . import db

from .models import Product
from .forms import ListingForm, validate_resell


market = Blueprint('market', __name__, url_prefix="/market")


@market.route("/post", methods=["GET", "POST"])
@login_required
def post_page():
    listing_form = ListingForm()

    if listing_form.validate_on_submit():
        productName = listing_form.productName.data
        productDescription = listing_form.productDescription.data
        productPrice = round(float(listing_form.productPrice.data), 2)

        g=github.Github(os.environ.get("GITT"))
        repo=g.get_repo("freemartimg")
        productImage = listing_form.productImage.data
        imageFilename = secure_filename(f'{productName.replace(" ", "-")}.{productImage.filename.split(".")[-1]}')
        with open(imageFilename, "rb") as image:
            f = image.read()
            image_data = bytearray(f)
        repo.create_file(imageFilename, "add new img", bytes(image_data), "master")

        item = Product(name=productName, description=productDescription, price=productPrice, imagePath=imagePath, user_id=current_user.id)
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
        valid, newProduct = validate_resell(productName, newPrice, current_user)

        if valid:
            product = Product.query.filter_by(name=productName).first()
            db.session.delete(product)
            db.session.commit()

            db.session.add(newProduct)
            db.session.commit()
        else:
            flash(newProduct, category="error")
            return redirect(url_for('user.profile_page'))

    items = Product.query.filter_by(listed=True)
    return render_template("market/market.html", user=current_user, items=items)
