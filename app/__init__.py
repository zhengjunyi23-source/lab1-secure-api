"""Application factory."""
from flask import Flask

from app.config import Config
from app.extensions import db


def seed_data():
    """Insert demo users on an empty database (for the educational example)."""
    from app.models import User

    if User.query.count() == 0:
        demo = [
            ("alice", "S3cure#Passw0rd", "admin", "I am the administrator."),
            ("bob", "Str0ng!Pa55", "user", "Just a regular user."),
            (
                "mallory",
                "M@llory2024",
                "user",
                # Intentionally unsafe input to demonstrate XSS escaping on output.
                "<script>alert('XSS')</script>",
            ),
        ]
        for username, password, role, about in demo:
            u = User(username=username, role=role, about=about)
            u.set_password(password)
            db.session.add(u)
        db.session.commit()


def create_app(config=None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    db.init_app(app)

    from app import routes  # noqa: E402  (register after db init)

    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()
        seed_data()

    return app
