from flask import Flask
from models import db


def create_app():
    """Application factory.

    Initializes the app and SQLAlchemy, and registers blueprints.
    Returns the configured Flask app.
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Import and register blueprints
    from routes import main as main_bp
    app.register_blueprint(main_bp)

    # Ensure DB tables exist in development
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
