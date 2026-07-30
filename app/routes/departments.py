from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.department import Department
from app.models.user import User

department_bp = Blueprint("departments", __name__)

def admin_required():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or user.role != "admin":
        return False

    return True

#GET all departments
@department_bp.route("/", methods=["GET"])
def get_departments():
    departments = Department.query.all()
    return jsonify([
        {
            "id": department.id,
            "name": department.name,
            "code": department.code,
            "description": department.description,
        }
        for department in departments
        ]), 200

#GET one department
@department_bp.route("/<int:department_id>", methods=["GET"])
def get_department(department_id):
    department = Department.query.get_or_404(id)
    return jsonify({
        "id": department.id,
        "name": department.name,
        "code": department.code,
        "description": department.description,
    }), 200

#POST a new department
@department_bp.route("/", methods=["POST"])
@jwt_required()
def create_department():

    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    data = request.get_json()


    if not data:
        return jsonify({"message": "Request body is required"}), 400

    required_fields = ["name", "code", "description"]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "message": f"{field} is required"
            }), 400

    existing_department = Department.query.filter_by(
        code=data["code"]
    ).first()

    if existing_department:
        return jsonify({
            "message": "Department code already exists"
        }), 409


    department = Department(
        name=data["name"],
        code=data["code"],
        description=data["description"]

    )

    db.session.add(department)
    db.session.commit()

    return jsonify({"message": "Department created successfully"}), 201

#PUT department 
@department_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_department(id):

    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    department = Department.query.get_or_404(id)
    data = request.get_json()

    department.name = data.get("name", department.name)
    department.code = data.get("code", department.code)
    department.description = data.get("description", department.description)

    db.session.commit()

    return jsonify({"message": "Department updated successfully"}), 200

#DELETE department
@department_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_department(id):

    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    department = Department.query.get_or_404(id)

    db.session.delete(department)
    db.session.commit()

    return jsonify({"message": "Department deleted successfully"}), 200
