from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from datetime import datetime

from . import db

from .models import User

from .forms import QuizForm

income = Blueprint('income', __name__, url_prefix="/income")

@login_required
@income.route("/quiz")
def quiz_page():
    user = User.query.filter_by(username=current_user.username).first()

    currentTime = datetime.utcnow()
    lastTime = datetime.strptime(user.lastquiz, '%Y-%m-%d %H:%M:%S.%f')
    difference = currentTime - lastTime


    if difference.days >= 1:
        user.lastquiz = currentTime
        db.session.commit()
        questionForm = QuizForm()
        if questionForm.validate_on_submit():
            return render_template(url_for("user.profile_page", username=current_user.username))
        return render_template("income/quiz.html", user=current_user, allow=True, form=questionForm)
    else:
        return render_template("income/quiz.html", user=current_user, allow=False, form=questionForm)
