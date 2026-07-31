from app.extensions import db


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)

    semester = db.Column(db.String(50), nullable=False)

    status = db.Column(
        db.String(20),
        default="Active",
        nullable=False
    )

    enrolled_on = db.Column(
        db.Date,
        server_default=db.func.current_date()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="enrollments"
    )

    course = db.relationship(
        "Course",
        back_populates="enrollments"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "semester": self.semester,
            "status": self.status,
            "enrolled_on": (
                self.enrolled_on.isoformat()
                if self.enrolled_on
                else None
            ),
            "user_id": self.user_id,
            "course_id": self.course_id,
        }

    def __repr__(self):
        return (
            f"<Enrollment {self.id} - "
            f"User {self.user_id} - "
            f"Course {self.course_id}>"
        )