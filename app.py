from flask import Flask
from models import db, User
from flask_login import LoginManager
import os

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Required to sign WTForms securely
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "a-very-secure-local-key")

    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, "project.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Redirect users here if a page requires them to be logged in
    login_manager.login_view = "main.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from routes import main as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
