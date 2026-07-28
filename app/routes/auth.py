from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db, bcrypt
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=hashed_password,
        role=data.get("role", "student")
    )

    db.session.add(new_user)
    db.session.commit() 

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    if not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify(
        {"access_token": access_token,
         "user": {
            "id": user.id,
            "name": f"{user.first_name} {user.last_name}",
            "role": user.role
         }})

@auth_bp.route("/profile", methods=["Get"])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role
        }
    ); 200

@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = user.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.email = data.get("email", user.email)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200