from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    prompts = [
        {
            "title": "Animal",
            "creator": "KevinAI",
            "rating": 4.8,
            "likes": 210,
            "image_url": "https://picsum.photos/400/600"
        },
        {
            "title": "Futuristic Samurai",
            "creator": "NeonCreator",
            "rating": 4.5,
            "likes": 180,
            "image_url": "https://picsum.photos/400/500"
        },
        {
            "title": "AI Dream Landscape",
            "creator": "PromptMaster",
            "rating": 4.9,
            "likes": 350,
            "image_url": "https://picsum.photos/400/700"
        },
        {
            "title": "Cyberpunk Cityscape",
            "creator": "Hacker",
            "rating": 3.8,
            "likes": 200,
            "image_url": "https://picsum.photos/400/800"
        },
        {
            "title": "photorealistic",
            "creator": "ProPrompter",
            "rating": 4.8,
            "likes": 4050,
            "image_url": "https://picsum.photos/400/900"
        },
        {
            "title": "Quality",
            "creator": "TopPrompter",
            "rating": 3.0,
            "likes": 30,
            "image_url": "https://picsum.photos/400/300"
        }
    ]
    return render_template("index.html", prompts=prompts)

@app.route("/trending")
def trending():
    return render_template("trending.html")

@app.route("/foryou")
def for_you():
    return render_template("foryou.html")

@app.route("/myprompts")
def my_prompts():
    return render_template("myprompts.html")

@app.route("/subscriptions")
def subscriptions():
    return render_template("subscriptions.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)