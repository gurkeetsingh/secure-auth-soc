from flask import Blueprint, jsonify, request
from app import db
from app.model import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() #using this to convert the json data to python data types like dictionary or list based on the data is json payload.

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # basic validation
    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400 # this will be returned if any of the information is missing because it will turn the if statement to true. The 400 at the end is the HTTP response status code which states that it is the bad request from the client side
    
    # check for existing user in database
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first() # this line of code query the User database and return the result if only if the condition inside the parenthesis meet because of the .filter. This line will return the first matching result from database. If there is no matching data then it return none
    if existing_user:
        return jsonify({"error":"Registration failed"}), 400

    # create a new user
    user = User(username=username , email = email)

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"success": "user registered successfully"}), 201


# coding a login logic

@auth_bp.route("/login", methods = ["POST"])
def login():
    data = request.get_json()

    #Input validation
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error":"Invalid credentials"}), 400 #If any of the data is missing then this error message will be shown to user
    
    email = data.get("email")
    password = data.get("password")

    # Fetch user from the database

    user = User.query.filter_by(email=email).first()

    # sending a generic message if a user is not found in a database

    if not user:
        return jsonify({"Error":"Invalid credentials"}), 401
    
    #Check the password hash safely

    if not check_password_hash(user.password_hash, data.get("password")):
        return jsonify({"error":"invalid credentials"}), 401
    
    # success response
    return jsonify({"Message":"login successful"})