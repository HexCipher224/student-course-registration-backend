from app import create_app
from app.extensions import db, bcrypt

from app.models.department import Department
from app.models.course import Course
from app.models.user import User
from app.models.enrollment import Enrollment

app = create_app()

with app.app_context():
    print("Clearing database...")

    Enrollment.query.delete()
    Course.query.delete()
    Department.query.delete()
    User.query.delete()

    db.session.commit()

    print("Creating departments...")

    computing = Department (
        name=" School of Computing",
        code="SCIT",
        description="Computer Science and IT"
    )

    business = Department (
        name="School of Business",
        code="SBUS",
        description="Business Administration"
    )

    db.session.add_all([computing, business])
    db.session.commit()

    print("Departments created!")

    print("Creating courses...")

    course1 = Course(
        title="Introduction to Programming",
        code="CSC101",
        credits=3,
        description="Python programming fundamentals",
        department_id=computing.id
    )

    course2 = Course(
        title="Database Systems",
        code="CSC202",
        credits=3,
        description="Relational Databases and SQL",
        department_id=computing.id
    )

    course3 = Course(
        title="Web Development",
        code="CSC203",
        credits=3,
        description="HTML, CSS, JavaScript and React",
        department_id=computing.id
    )

    db.session.add_all([course1, course2, course3])
    db.session.commit()

    print("Courses created!")

    print("Creating users...")

    admin = User(
        first_name="Admin",
        last_name="User",
        email="admin@example.com",
        password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
        role="admin"
    )

    student = User(
        first_name="Duncan",
        last_name="Munene",
        email="duncan@example.com",
        password=bcrypt.generate_password_hash("12345678").decode("utf-8"),
        role="student"
    )

    db.session.add_all([admin, student])
    db.session.commit()

    print("Users created!")

    print("Creating enrollments...")

    enrollment1 = Enrollment(
        semester="2026 Semester 1",
        status="Active",
        user_id=student.id,
        course_id=course1.id
    )

    enrollment2 = Enrollment(
        semester="2026 Semester 1",
        status="Active",
        user_id=student.id,
        course_id=course2.id
    )

    db.session.add_all([enrollment1, enrollment2])
    db.session.commit()

    print("Enrollments created!")