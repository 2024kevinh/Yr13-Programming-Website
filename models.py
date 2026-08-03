from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    subscription_type = db.Column(db.String(20), default="Free")
    generations_today = db.Column(db.Integer, default=0)
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    prompts = db.relationship("Prompt", back_populates="user")


class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    creator = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    likes = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(300))
    uploaded_image = db.Column(db.String(255), nullable=True)

    user = db.relationship("User", back_populates="prompts")


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey("prompt.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "prompt_id"),
    )


class Generation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'))


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    reason = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class SavedPrompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey("prompt.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "prompt_id"),
    )
