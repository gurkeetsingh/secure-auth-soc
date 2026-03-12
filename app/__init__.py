from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

load_dotenv()

db = SQLAlchemy()

print(os.getenv("JWT_SECRET_KEY")) #add this into comment after testing

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    print("DATABASE_URL =", os.getenv("DATABASE_URL"))
    db.init_app(app)

    jwt = JWTManager(app)

    with app.app_context():
        from app.model import User
        db.create_all()

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
