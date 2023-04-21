# Importing 3rd party components
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from sqlalchemy import func

from passlib.hash import pbkdf2_sha256

# Importing freemart components
from . import db

from .models import User

from .forms import LoginForm, RegisterForm

from .helperFunc import generateToken, validateToken, sendConfirmationEmail, deleteAccount


# Auth branch blueprint definition
auth = Blueprint('auth', __name__, url_prefix="/auth")


# ----- Routes definition ----- #

@auth.route("/confirm/<token>")
@login_required
def confirm_hollow_page(token):
    '''
        Verify a email confirmation link.
        Redirect to profile page.
        Flash an appropriate [success, warning or error] message
    '''

    if current_user.confirmed:
        flash("Account already active", category="warning")
    else:
        if validateToken(token):
            current_user.confirmed = True
            print('yes')
            db.session.commit()
            flash(f"Welcome, {current_user.username}!", category="success")
        else:
            flash("Invalid/Expired link", category="error")
    return redirect(url_for("user.profile_page", username=current_user.username))


@auth.route("/delete/<token>")
def delete_hollow_page(token):
    outcome = deleteAccount(token)
    if outcome == True:
        flash('Account deleted', category='success')
    else:
        flash(outcome, category='error')
    return redirect(url_for('auth.login_page'))


@auth.route("/resend_confirm")
@login_required
def resend_confirm_hollow_page():
    '''
        Resend confirmation email.
        Redirct to unconfirmed page.
    '''

    sendConfirmationEmail(current_user)

    return redirect(url_for("auth.unconfirmed_page"))


@auth.route('/unconfirmed_page')
@login_required
def unconfirmed_page():
    '''
        Inform user they must activate account.
        Link to resend email.
        Redirect confirmed user to profile page.
    '''

    if current_user.confirmed:
        flash("Account already active", category="warning")
        return redirect(url_for('user.profile_page', username=current_user.username))
    return render_template("auth/unconfirmed.html", user=current_user)


@auth.route("/login", methods=["GET", "POST"])
def login_page():
    '''
        Login user.
        If user is not confirmed send email.
        Redirect to profile page.
    '''

    if current_user.is_authenticated:
        return redirect(url_for("user.profile_page", username=current_user.username))
    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        # Case insensitive username look-up
        user = User.query.filter(func.lower(User.username)==func.lower(username)).first()
        login_user(user, remember=True)

        if not current_user.confirmed:
            sendConfirmationEmail(current_user)
        return redirect(url_for("user.profile_page", username=current_user.username))
    return render_template("auth/login.html", user=current_user, form=login_form)


@auth.route('/logout')
@login_required
def logout_page():
    '''
        Logout user.
    '''
    logout_user()
    return redirect(url_for('auth.login_page'))


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up_page():
    '''
        Register a new user & send email.
        Redirect to profile page.
    '''

    if current_user.is_authenticated:
        return redirect(url_for("user.profile_page", username=current_user.username))
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        username = register_form.username.data.strip()
        email = register_form.email.data.lower().strip()
        password = register_form.password.data

        user = User(username=username, email=email, password=pbkdf2_sha256.hash(password))
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)

        sendConfirmationEmail(current_user)

        return redirect(url_for("user.profile_page", username=current_user.username))
    return render_template("auth/sign-up.html", user=current_user, form=register_form)
