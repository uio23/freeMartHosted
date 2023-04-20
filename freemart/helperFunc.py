# Importing 3rd party components
from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_mail import Message

import numpy as np

from itsdangerous import URLSafeTimedSerializer

from functools import wraps

import os

# Importing freemart components
from . import mail

from .models import User


def isFloat(variable: str) -> bool:
    '''
    Check if a variable holds float value
    '''

    try:
        float(variable)
        return True
    except ValueError:
        return False


def removeOutliers(numList: list) -> list[int]:
    '''
    Clean a numerical list from extream outlier values\n
    (iqr * 3.5)
    '''

    cleanedList = []

    try:
        processedList = sorted([float(x) for x in numList])
    except ValueError:
        raise ValueError('List must hold numerical values')

    try:
        upper_q = np.percentile(processedList, 75)
        lower_q = np.percentile(processedList, 25)
    except IndexError:
        raise IndexError('Cannot remove outliers from an empty list')

    iqr = (upper_q - lower_q) * 3.5
    q_set = (lower_q - iqr, upper_q + iqr)
    for price in processedList:
        if price >= q_set[0] and price <= q_set[1]:
            cleanedList.append(price)
    return cleanedList


def generateToken(email: str) -> str:
    '''
        Encode given email into a secure token
    '''

    serializer = URLSafeTimedSerializer(os.environ.get('MONKEY'))
    token = serializer.dumps(email, salt=os.environ.get('MONKEY_PASS'))
    return token


def validateToken(token: str, expiration=3600):
    '''
        Confirm if given token de-codes to current user's email
    '''

    serializer = URLSafeTimedSerializer(os.environ.get('MONKEY'))
    try:
        email = serializer.loads(token, salt=os.environ.get('MONKEY_PASS'), max_age=expiration)
        print(email)
    except:
        return False
    user = User.query.filter_by(email=current_user.email).first()
    print(user)
    if user.email == email:
        return True
    return False


def sendConfirmationEmail(user: User) -> None:
    '''
        Send user email with token, to activate their account
    '''

    token = generateToken(user.email)
    url = url_for("auth.confirm_hollow_page", token=token, _external=True)
    contentHtml = render_template("auth/confirmationEmail.html", username=user.username, url=url)
    msg = Message(sender=os.environ.get("MAIL_DEFAULT_SENDER"), recipients=[user.email], subject="Activate Your Free Mart Account", html=contentHtml)
    mail.send(msg)


def confirmed_required(func):
    '''
        Redirect to unconfirmed page if user unconfirmed.
    '''

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            return redirect(url_for('auth.unconfirmed_page'))
        return func(*args, **kwargs)
    return decorated_function
