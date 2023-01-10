from flask import Blueprint, redirect, render_template, flash, url_for, current_app, request
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

from github import Github

import os

import io
from PIL import Image

from . import db

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from .models import Product
from .forms import ListingForm, validate_resell


market = Blueprint('market', __name__, url_prefix="/market")

g = Github("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")

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
        img = Image.open(productImage)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        for repo in g.get_user().get_repos():
            if repo.name == "freemart_img":
                repo.create_file(imageFilename, "Img added", bytes(img_byte_arr), "main")

        item = Product(name=productName, description=productDescription, price=productPrice, imagePath=imageFilename, user_id=current_user.id)
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
