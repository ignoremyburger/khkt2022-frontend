from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_login import UserMixin

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    hashed_password = db.Column(db.String(), nullable=False, unique=False)
