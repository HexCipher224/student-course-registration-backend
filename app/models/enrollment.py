from app.extensions import db


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(20), nullable=False, unique=True)
    credits = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    department = db.relationship("Department", back_populates="courses")

    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")