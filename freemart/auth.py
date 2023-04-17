from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from passlib.hash import pbkdf2_sha256

from . import db

from sqlalchemy import func

from .models import User

from .forms import LoginForm, RegisterForm

from .helperFunc import generateToken, validateToken, sendEmail


auth = Blueprint('auth', __name__, url_prefix="/auth")

@auth.route("/confirm/<token>")
@login_required
def confirm_page(token):
    email = validateToken(token)
    user = User.query.filter_by(email=current_user.email).first()
    if current_user.confirmed:
        flash("Account already confirmed", "success")
        return redirect(url_for("user.profile_page", username=current_user.username))

    if user.email == email:
        user.confirmed = True
        db.session.commit()
        flash(f"Welcome, {current_user.username}!", category="success")
    else:
        flash("Invalid confirmation link", "error")
    return redirect(url_for("user.profile_page", username=current_user.username))


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

@auth.route('/unconfirmed_page')
@login_required
def unconfirmed_page():
    token = generateToken(current_user.email)
    confirm_url = url_for("auth.confirm_page", token=token, _external=True)
    html = render_template("auth/confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    sendEmail(current_user.email, subject, html)
    return render_template("auth/unconfirmed.html", user=current_user)

@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up_page():
    if current_user.is_authenticated:
        return redirect(url_for("user.profile_page", username=current_user.username))


    register_form = RegisterForm()

    if register_form.validate_on_submit():
        username = register_form.username.data.strip()
        email = register_form.email.data.lower().strip()
        password = register_form.password.data

        user = User(username=username, password=pbkdf2_sha256.hash(password))
        db.session.add(user)
        db.session.commit()

        token = generateToken(email)
        confirm_url = url_for("auth.confirm_page", token=token, _external=True)
        html = render_template("auth/confirm_page.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        sendEmail(user.email, subject, html)

        login_user(user, remember=True)

        return redirect(url_for("user.profile_page", username=current_user.username))

    return render_template("auth/sign-up.html", user=current_user, form=register_form)
