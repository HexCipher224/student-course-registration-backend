from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.course import Course
from app.models.user import User
from app.models.department import Department

course_bp = Blueprint("courses", __name__)

def admin_required():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or user.role != "admin":
        return False

    return True


#Get all courses
@course_bp.route("/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([
        {
            "id": course.id,
            "title": course.title,
            "credits": course.credits,
            "code": course.code,
            "description": course.description,
            "department_id": course.department_id
        }
        for course in courses
        ]), 200

#Create a course
@course_bp.route("/", methods=["POST"])
@jwt_required()
def create_course():

    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body is required"}), 400

    required_fields = [
        "title",
        "code",
        "credits",
        "description",
        "department_id"
    ]

    for field in required_fields:
        if data.get(field) is None:
            return jsonify({
                "message": f"{field} is required"
            }), 400

    existing_course = Course.query.filter_by(
        code=data["code"]
    ).first()

    if existing_course:
        return jsonify({
            "message": "Course code already exists"
        }), 409

    department = Department.query.get(data["department_id"])

    if not department:
        return jsonify({
            "message": "Department not found"
        }), 404


    course = Course(
        title=data["title"],
        code=data["code"],
        credits=data["credits"],
        description=data.get("description"),
        department_id=data["department_id"]
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({"message": "Course created successfully"}), 201

#Get a course by 
@course_bp.route("/<int:id>", methods=["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify({
        "id": course.id,
        "title": course.title,
        "credits": course.credits,
        "code": course.code,
        "description": course.description,
        "department_id": course.department_id
    }), 200

#Update a course
@course_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_course(id):
    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403
    
    course = Course.query.get_or_404(id)
    data = request.get_json()

    course.title = data.get("title", course.title)
    course.code = data.get("code", course.code)
    course.credits = data.get("credits", course.credits)
    course.description = data.get("description", course.description)
    course.department_id = data.get("department_id", course.department_id)

    db.session.commit()

    return jsonify({"message": "Course updated successfully"}), 200

#Delete a course
@course_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_course(id):
    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return jsonify({"message": "Course deleted successfully"}),