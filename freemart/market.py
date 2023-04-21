# Importing 3rd party components
from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

import random

import math

import os

# Importing freemart component
from . import db

from .models import Product

from .forms import PostForm

from .imageFunc import saveImg, loadImgs

from .bonusFunc import calcSaleBonus

from .helperFunc import confirmed_required


# Market branch blueprint definition
market = Blueprint('market', __name__, url_prefix="/market")


# ----- Routes definition ----- #

@market.route("/post", methods=["GET", "POST"])
@login_required
@confirmed_required
def post_page():
    '''
        Let user post a new item.
    '''

    postForm = PostForm()

    # Minimum to recieve bonus calculated now for user aid
    minForBonus = 0

    if current_user.sale_count <= 7:
        minForBonus = int(calcSaleBonus(current_user)/4)

    if postForm.validate_on_submit():
        productName = postForm.productName.data.strip()
        productDescription = postForm.productDescription.data.strip()
        productPrice =  math.floor(float(postForm.productPrice.data) * 10 ** 2) / 10 ** 2
        productImage = postForm.productImage.data
        imageFilename = secure_filename(f'{productName.replace(" ", "-")}.{productImage.filename.split(".")[-1]}')

        if not saveImg(productImage, imageFilename):
            flash("Failed to upload image", category="error")
            return render_template("market/post.html", user=current_user, form=postForm)

        item = Product(name=productName, description=productDescription, price=productPrice, imagePath=imageFilename, username=current_user.username)
        db.session.add(item)
        db.session.commit()

        return redirect(url_for('market.market_page', product=item.name))

    return render_template("market/post.html", user=current_user, minForBonus=minForBonus, form=postForm)


@market.route("/market", methods=["GET", "POST"])
@market.route("/", methods=["GET", "POST"])
@login_required
@confirmed_required
def market_page():
    '''
        Display all items for purchase.
    '''

    items = Product.query.filter_by(listed=True).all()
    random.shuffle(items)

    product = request.args.get('product', None);
    if product:
        itemNames = [item.name for item in items]
        productLoc = itemNames.index(product)
        items.insert(0, items.pop(productLoc))
    groupedItems = []

    loadImgs(items)

    for i in range(0, len(items), 6):
        groupedItems.append(items[i:i+6])

    return render_template("market/market.html", user=current_user, items=groupedItems)
