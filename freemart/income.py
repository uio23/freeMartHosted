from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from datetime import datetime

from decimal import Decimal

from . import db

from .models import User

from .forms import QuizForm


income = Blueprint('income', __name__, url_prefix="/income")


@login_required
@income.route("/quiz", methods=["GET", "POST"])
def quiz_page():
    user = current_user

    currentTime = datetime.utcnow()
    lastTime = datetime.strptime(user.lastquiz, '%Y-%m-%d %H:%M:%S.%f')
    difference = currentTime - lastTime


    if difference.days >= 1:
        questionForm = QuizForm()
        if questionForm.validate_on_submit():
            user.lastquiz = currentTime
            answers = [questionForm.qOne.data, questionForm.qTwo.data, questionForm.qThree.data]
            numOfCorrect = 0
            checked = []
            outcome = []
            for index, answer in enumerate(answers):
                if answer == "True":
                    checked.append("checked")
                    checked.append("")
                else:
                    checked.append("")
                    checked.append("checked")

                if answer == questionForm.questions[index][1]:
                    numOfCorrect += 1
                    outcome.append("valid")
                else:
                    outcome.append("invalid")
            quizBonus = calcQuizBonus(user)
            user.balance += numOfCorrect*10
            db.session.commit()

            return render_template("income/quizResult.html", user=current_user, outcome=outcome, checked=checked, numOfCorrect=numOfCorrect, form=questionForm)
        return render_template("income/quiz.html", user=current_user, allow=True, form=questionForm)
    else:
        return render_template("income/quiz.html", user=current_user, allow=False)
