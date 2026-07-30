from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.enrollment import Enrollment
from app.models.course import Course
from app.models.user import User


enrollment_bp = Blueprint("enrollments", __name__)

#Get all enrollments
@enrollment_bp.route("/", methods=["GET"])
def get_enrollments():
    enrollments = Enrollment.query.all()

    return jsonify([
        {
            "id": enrollment.id,
            "user_id": enrollment.user_id,
            "course_id": enrollment.course_id,
            "status": enrollment.status
        }
        for enrollment in enrollments
    ])

#Create an enrollment
@enrollment_bp.route("/", methods=["POST"])
@jwt_required()
def create_enrollment():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    required_fields = [
        "user_id",
        "course_id",
        "semester"
    ]

    for field in required_fields:
        if data.get(field) is None:
            return jsonify({
                "message": f"{field} is required"
                }), 400

    user = User.query.get(data["user_id"])

    if not user:
        return jsonify({"message": "User not found"}), 404

    course = Course.query.get(data["course_id"])

    if not course:
        return jsonify({"message": "Course not found"}), 404

    existing = Enrollment.query.filter_by(
        user_id=data["user_id"],
        course_id=data["course_id"],
        semester=data["semester"]
    ).first()

    if existing:
        return jsonify({
            "message": "Student is already enrolled in this "
        }), 409
        
    enrollment = Enrollment(
        user_id=data["user_id"],
        course_id=data["course_id"],
        semester=data["semester"],
        status=data.get("status", "Active")
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({"message": "Enrollment created successfully"}), 201

#Update an enrollment
@enrollment_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    data = request.get_json()

    enrollment.status = data.get("status", enrollment.status)

    db.session.commit()

    return jsonify({"message": "Enrollment updated successfully"}), 200

#Delete an enrollment
@enrollment_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)

    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({"message": "Enrollment deleted successfully"}), 200