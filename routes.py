from flask import Blueprint, render_template
from models import Prompt

main = Blueprint("main", __name__)


@main.route("/")
def home():
    # Query prompts from the database. Templates expect attributes like
    # prompt.image_url, prompt.title, prompt.creator,
    # prompt.rating, prompt.likes
    prompts = Prompt.query.order_by(Prompt.likes.desc()).all()
    return render_template("index.html", prompts=prompts)


@main.route("/trending")
def trending():
    return render_template("trending.html")


@main.route("/foryou")
def for_you():
    return render_template("foryou.html")


@main.route("/myprompts")
def my_prompts():
    return render_template("myprompts.html")


@main.route("/subscriptions")
def subscriptions():
    return render_template("subscriptions.html")


@main.route("/settings")
def settings():
    return render_template("settings.html")


@main.route("/login")
def login():
    return render_template("login.html")


@main.route("/signup")
def signup():
    return render_template("signup.html")
