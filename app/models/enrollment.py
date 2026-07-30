from app.models.enrollment import Enrollment

@course_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_course(id):
    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    course = Course.query.get_or_404(id)

    enrollment = Enrollment.query.filter_by(course_id=id).first()

    if enrollment:
        return jsonify({
            "message": "Cannot delete course because students are enrolled."
        }), 400

    db.session.delete(course)
    db.session.commit()

    return jsonify({
        "message": "Course deleted successfully"
    }), 200