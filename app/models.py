"""Database models.

Passwords are stored ONLY as bcrypt hashes, never in plaintext.
All queries go through the SQLAlchemy ORM, so user input is always bound
as parameters (protection against SQL injection).
"""
import bcrypt
from app.extensions import db


class User(db.Model):
    """Application user account."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")
    about = db.Column(db.Text, nullable=False, default="")

    def set_password(self, raw_password: str) -> None:
        """Hash a plaintext password with bcrypt and store only the hash."""
        self.password_hash = bcrypt.hashpw(
            raw_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        """Compare a supplied password against the stored bcrypt hash."""
        try:
            return bcrypt.checkpw(
                raw_password.encode("utf-8"), self.password_hash.encode("utf-8")
            )
        except ValueError:
            return False

    def to_public_dict(self) -> dict:
        """Public representation of the user. Never exposes the hash."""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "about": self.about,
        }
