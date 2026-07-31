from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User

user_bp = Blueprint("users", __name__)


def admin_required():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    return user and user.role == "admin"


@user_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():

    if not admin_required():
        return jsonify({
            "message": "Admin access required"
        }), 403

    users = User.query.all()

    return jsonify([
        {
            "id": user.id,
            "name": getattr(user, "name", None),
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]), 200