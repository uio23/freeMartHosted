from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from datetime import datetime

from . import db

from .models import User

income = Blueprint('income', __name__, url_prefix="/income")

@login_required
@income.route("/quiz")
def quiz_page():
    user = User.query.filter_by(username=current_user.username).first()
    difference = datetime.utcnow() - user.lastquiz
    print(datetime.utcnow())
    print(user.lastquiz)
    if difference.days >= 1:
        return render_template("Yes sir")
    else:
        return render_template("Huh")
