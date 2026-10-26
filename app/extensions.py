"""SQLAlchemy instance shared across the application (avoids circular imports)."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
