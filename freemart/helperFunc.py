import numpy as np

from itsdangerous import URLSafeTimedSerializer

from flask_mail import Message

from functools import wraps

from flask import flash, url_for, redirect

from flask_login import current_user

import os

from . import mail


def isFloat(variable: str) -> bool:
    '''
    Check if a string holds float value
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
    serializer = URLSafeTimedSerializer(os.environ.get('MONKEY'))
    token = serializer.dumps(email, salt=os.environ.get('MONKEY_PASS'))
    return token


def validateToken(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.environ.get('MONKEY'))
    # try:
    email = serializer.loads(token, salt=os.environ.get('MONKEY_PASS'), max_age=expiration)
    return email
    # except Exception
        # return False

def sendEmail(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender=os.environ.get("MAIL_DEFAULT_SENDER"))
    mail.send(msg)


def confirmed_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            return redirect(url_for('auth.unconfirmed_page'))
        return func(*args, **kwargs)

    return decorated_function
