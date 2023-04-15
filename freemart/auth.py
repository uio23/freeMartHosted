from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from passlib.hash import pbkdf2_sha256

from . import db

from sqlalchemy import func

from .models import User

from .forms import LoginForm, RegisterForm


auth = Blueprint('auth', __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("user.profile_page", username=current_user.username))


    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        user = User.query.filter(func.lower(User.username)==func.lower(username)).first()

        login_user(user, remember=True)

        return redirect(url_for("user.profile_page", username=current_user.username))

    return render_template("auth/login.html", user=current_user, form=login_form)


@auth.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('auth.login_page'))


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up_page():
    if current_user.is_authenticated:
        return redirect(url_for("user.profile_page", username=current_user.username))


    register_form = RegisterForm()

    if register_form.validate_on_submit():
        username = register_form.username.data
        username = username.strip()
        password = register_form.password.data

        user = User(username=username, password=pbkdf2_sha256.hash(password))
        db.session.add(user)
        db.session.commit()

        flash(f"Welcome, {username}!", category="success")
        login_user(user, remember=True)

        return redirect(url_for("user.profile_page", username=current_user.username))

    return render_template("auth/sign-up.html", user=current_user, form=register_form)
