from flask import Flask
from models import db
import os


def create_app():
    """Application factory.

    Initializes the app and SQLAlchemy, and registers blueprints.
    Returns the configured Flask app.
    """
    app = Flask(__name__)
    # if present; we do not automatically copy or move any other DB files.
    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, "project.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Helpful debug note: DB path is explicit to avoid path confusion

    # Import and register blueprints
    from routes import main as main_bp
    app.register_blueprint(main_bp)

    # Ensure DB tables exist in development
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
