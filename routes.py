from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, Prompt, User
from forms import LoginForm, SignUpForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint("main", __name__)

@main.route("/")
def home():
    prompts = Prompt.query.order_by(Prompt.likes.desc()).all()
    return render_template("index.html", prompts=prompts)


@main.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    form = SignUpForm()
    if form.validate_on_submit():
        # Scrypt hashes the password securely before saving to project.db
        hashed_password = generate_password_hash(form.password.data, method="scrypt")
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("main.login"))
        
    return render_template("signup.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            # Simple error fallback, can style a flash container later
            form.email.errors.append("Invalid email or password.")
            
    return render_template("login.html", form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@main.route("/trending")
def trending(): return render_template("trending.html")


@main.route("/foryou")
def for_you(): return render_template("foryou.html")


@main.route("/myprompts")
def my_prompts(): return render_template("myprompts.html")


@main.route("/subscriptions")
def subscriptions(): return render_template("subscriptions.html")


@main.route("/settings")
def settings(): return render_template("settings.html")

