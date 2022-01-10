
from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    Username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Surname = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(25), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Language = db.Column(db.String(20), nullable=False)


