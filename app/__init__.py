from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print("DATABASE_URL =", os.getenv("DATABASE_URL"))
    db.init_app(app)

    with app.app_context():
        from app.model import User
        db.create_all()

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
