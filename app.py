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
        }
    ]
    return render_template("index.html", prompts=prompts)

if __name__ == "__main__":
    app.run(debug=True)