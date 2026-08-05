from app import create_app
from models import db, Prompt, User


def seed_prompts(default_user_id):
    example = [
        {
            "title": "Cat",
            "description": "A detailed prompt to generate realistic animal imagery.",
            "prompt_text": "Placeholder prompt",
            "image_url": "images/Cat.jpg",
            "likes": 4,
        },
        {
            "title": "Photography",
            "description": "Stylised portrait scene with neon lights.",
            "prompt_text": "Placeholder prompt",
            "image_url": "images/Women.jpg",
            "likes": 5,
        },
        {
            "title": "Strawberry",
            "description": "Close up of a fruit with water droplets.",
            "prompt_text": "Placeholder prompt",
            "image_url": "images/Strawberry.jpg",
            "likes": 4,
        },
        {
            "title": "Cyberpunk Cityscape",
            "description": "Cyberpunk city at night with neon signs.",
            "prompt_text": "Placeholder prompt",
            "image_url": "images/CyberpunkCityScape.jpg",
            "likes": 3,
        },
        {
            "title": "Parrot",
            "description": "High-quality photorealistic animal prompt.",
            "prompt_text": "Placeholder prompt",
            "image_url": "images/Parrot.jpg",
            "likes": 5,
        },
        {
            "title": "Cyberpunk",
            "description": "Street scene with neon lights.",
            "prompt_text": "Placeholder prompt",
            "image_url": "images/Cyberpunk.jpeg",
            "likes": 3,
        },
    ]

    for p in example:
        exists = (
            Prompt.query.filter_by(title=p["title"], creator=default_user_id).first()
        )
        if not exists:
            prompt = Prompt(
                title=p["title"],
                description=p["description"],
                prompt_text=p["prompt_text"],
                image_url=p["image_url"],
                creator=default_user_id,
                likes=p["likes"],
            )
            db.session.add(prompt)
    db.session.commit()


def main():
    app = create_app()
    with app.app_context():
        # Create tables for the current models
        db.create_all()

        # Ensure a default user exists to assign as the prompt creator
        default_username = "seed_user"
        default_email = "seed@example.com"
        user = User.query.filter_by(username=default_username).first()
        if not user:
            user = User(username=default_username,
                        email=default_email,
                        password_hash="seed")
            db.session.add(user)
            db.session.commit()

        seed_prompts(user.id)
        print("Database created/updated and sample prompts seeded.")


if __name__ == "__main__":
    main()
