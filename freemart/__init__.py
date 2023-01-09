from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
from flask_login import LoginManager, current_user, current_user

import os


db = SQLAlchemy()
DB_NAME = 'database.db'


login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
            ), 'static/productImages'
        )
    app.secret_key = 'replace'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres uri"


    from .auth import auth
    from .market import market
    from .user import user

    app.register_blueprint(user)
    app.register_blueprint(market)
    app.register_blueprint(auth)


    db.init_app(app)
    login_manager.login_view = 'auth.login_page'
    login_manager.init_app(app)


    from .models import User, Product, Message


    @login_manager.user_loader
    def load_user(id):
        return User.get(id)


    @app.route("/")
    @app.route("/home")
    def home_page():
        return render_template("home.html", user=current_user)


    from .models import Message

    socketio = SocketIO(app)
    @socketio.on('message')
    def message(data):
        if db.session.query(Message).count() >50:
            oldestMessage = db.session.query(Message).first()
            db.session.delete(oldestMessage)

        if data["auth"]:
            print(f"\n\n > {data['username']} connected to the chatroom. \n\n")
        elif data["msg"] == '':
            pass
        else:
            send(data)
            message = Message(msg=data['msg'], username=data["username"])
            db.session.add(message)
        db.session.commit()

    return app, socketio
