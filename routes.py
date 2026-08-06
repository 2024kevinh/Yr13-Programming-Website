from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from models import db, Prompt, User, SavedPrompt, Like
from forms import LoginForm, SignUpForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint("main", __name__)


@main.route("/")
def home():
    prompts = Prompt.query.order_by(Prompt.likes.desc()).all()

    saved_ids = set()
    liked_ids = set()

    if current_user.is_authenticated:

        saved_ids = {
            save.prompt_id
            for save in SavedPrompt.query.filter_by(
                user_id=current_user.id
            ).all()
        }

        liked_ids = {
            like.prompt_id
            for like in Like.query.filter_by(
                user_id=current_user.id
            ).all()
        }

    return render_template(
        "index.html",
        prompts=prompts,
        saved_ids=saved_ids,
        liked_ids=liked_ids
    )


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
def trending():
    prompts = Prompt.query.order_by(
        Prompt.likes.desc()
    ).all()

    saved_prompts = set()
    liked_prompts = set()

    if current_user.is_authenticated:
        saved_prompts = {
            save.prompt_id
            for save in SavedPrompt.query.filter_by(
                user_id=current_user.id
            ).all()
        }

        liked_prompts = {
            like.prompt_id
            for like in Like.query.filter_by(
                user_id=current_user.id
            ).all()
        }

    return render_template(
        "trending.html",
        prompts=prompts,
        saved_prompts=saved_prompts,
        liked_prompts=liked_prompts
    )


@main.route("/savedprompts")
def saved_prompts():
    saved_prompts = []
    if current_user.is_authenticated:
        saved_records = SavedPrompt.query.filter_by(
            user_id=current_user.id
        ).all()

        saved_prompts = [
            Prompt.query.get(save.prompt_id)
            for save in saved_records
        ]

    return render_template(
        "savedprompts.html",
        saved_prompts=saved_prompts
    )


@main.route("/myprompts")
@login_required
def my_prompts():
    return render_template("myprompts.html")


@main.route("/subscriptions")
def subscriptions(): return render_template("subscriptions.html")


@main.route("/settings")
def settings(): return render_template("settings.html")


@main.route("/save_prompt/<int:prompt_id>", methods=["POST"])
def save_prompt(prompt_id):

    if not current_user.is_authenticated:
        return jsonify({
            "error": "Please login to save prompts."
        }), 401

    saved = SavedPrompt.query.filter_by(
        user_id=current_user.id,
        prompt_id=prompt_id
    ).first()

    if saved:
        db.session.delete(saved)
        db.session.commit()
        return jsonify({"saved": False})

    new_save = SavedPrompt(
        user_id=current_user.id,
        prompt_id=prompt_id
    )

    db.session.add(new_save)
    db.session.commit()

    return jsonify({"saved": True})


@main.route("/like_prompt/<int:prompt_id>", methods=["POST"])
def like_prompt(prompt_id):

    if not current_user.is_authenticated:
        return jsonify({
            "error": "Please login to like prompts."
        }), 401

    liked = Like.query.filter_by(
        user_id=current_user.id,
        prompt_id=prompt_id
    ).first()

    prompt = Prompt.query.get_or_404(prompt_id)

    if liked:
        db.session.delete(liked)
        prompt.likes -= 1
        db.session.commit()

        return jsonify({
            "liked": False,
            "likes": prompt.likes
        })

    new_like = Like(
        user_id=current_user.id,
        prompt_id=prompt_id
    )

    db.session.add(new_like)
    prompt.likes += 1
    db.session.commit()

    return jsonify({
        "liked": True,
        "likes": prompt.likes
    })


@main.route("/prompt/<int:prompt_id>", methods=["GET", "POST"])
def prompt_detail(prompt_id):

    prompt = Prompt.query.get_or_404(prompt_id)

    saved_prompts = set()
    liked_prompts = set()

    if current_user.is_authenticated:

        saved_prompts = {
            save.prompt_id
            for save in SavedPrompt.query.filter_by(
                user_id=current_user.id
            ).all()
        }

        liked_prompts = {
            like.prompt_id
            for like in Like.query.filter_by(
                user_id=current_user.id
            ).all()
        }

    if request.method == "POST":
        # Image upload logic goes here
        pass

    return render_template(
        "prompt_detail.html",
        prompt=prompt,
        saved_prompts=saved_prompts,
        liked_prompts=liked_prompts
    )
