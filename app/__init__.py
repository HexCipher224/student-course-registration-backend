from flask import Flask

from .config import Config
from .extensions import db, jwt, bcrypt, cors
from flask_migrate import Migrate
from .models import User, Department, Course, Enrollment

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    from .routes import auth_bp, department_bp 

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    app.register_blueprint(
        department_bp,
        url_prefix="/api/departments"
    )

    @app.route("/")
    def home():
        return {
            "message": "Student Course Registration API is running!"
        }

   

    return app