"""Models for Notes app"""

# import bcrypt
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True)
    username = db.Column(db.String(20), primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/ hashed password and return user"""
        
        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username,
                   password=hashed,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that the user exists and password is correct.
            Return user if valid, else return false.
        """

        user_instance = cls.query.filter_by(username=username).one_or_none()
        if user_instance and bcrypt.check_password_hash(
                user_instance.password,
                password):
            return user_instance
        else:
            return False


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
