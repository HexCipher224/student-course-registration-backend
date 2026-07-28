from flask import Blueprint 
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.course import Course

course_bp = Blueprint("courses", __name__)

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
    data = request.get_json()

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
    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return jsonify({"message": "Course deleted successfully"}),