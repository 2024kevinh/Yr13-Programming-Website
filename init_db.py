"""Small helper to create the DB and seed example Prompt rows.

Run with: python init_db.py
"""
from app import create_app
from models import db, Prompt


def seed_prompts():
    example = [
        {
            "title": "Animal",
            "creator": "KevinAI",
            "rating": 4.8,
            "likes": 210,
            "image_url": "https://picsum.photos/400/600",
        },
        {
            "title": "Futuristic Samurai",
            "creator": "NeonCreator",
            "rating": 4.5,
            "likes": 180,
            "image_url": "https://picsum.photos/400/500",
        },
        {
            "title": "AI Dream Landscape",
            "creator": "PromptMaster",
            "rating": 4.9,
            "likes": 350,
            "image_url": "https://picsum.photos/400/700",
        },
        {
            "title": "Cyberpunk Cityscape",
            "creator": "Hacker",
            "rating": 3.8,
            "likes": 200,
            "image_url": "https://picsum.photos/400/600",
        },
        {
            "title": "Photorealistic",
            "creator": "ProPrompter",
            "rating": 4.8,
            "likes": 4050,
            "image_url": "https://picsum.photos/400/400",
        },
        {
            "title": "Quality",
            "creator": "TopPrompter",
            "rating": 3.0,
            "likes": 30,
            "image_url": "https://picsum.photos/400/300",
        },
    ]

    for p in example:
        # Only add if the same title/creator pair doesn't already exist
        exists = (
            Prompt.query.filter_by(
                title=p["title"], creator=p["creator"]
            ).first()
        )
        if not exists:
            prompt = Prompt(
                title=p["title"],
                creator=p["creator"],
                rating=p["rating"],
                likes=p["likes"],
                image_url=p["image_url"],
            )
            db.session.add(prompt)
    db.session.commit()


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_prompts()
        print("Database created/updated and sample prompts seeded.")


if __name__ == "__main__":
    main()
