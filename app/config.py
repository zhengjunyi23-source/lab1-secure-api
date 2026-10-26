"""Application configuration."""
import os


class Config:
    """Central configuration loaded from environment variables with sane defaults."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-secret-key-change-in-production")
    JWT_EXPIRES_MINUTES = int(os.environ.get("JWT_EXPIRES_MINUTES", "60"))
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
