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


class Position(db.Model, UserMixin):
    CityCode = db.Column(db.String(5), nullable=False, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Province = db.Column(db.String(20), nullable=False)
    Nation = db.Column(db.String(20), nullable=False)
    Zone = db.Column(db.String(20), nullable=False)

    # def __repr__(self):
    #   return "Position('{self.Zone}')"


class Event(db.Model, UserMixin):
    Number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(20), nullable=False)
    Organiser = db.Column(db.String(20), nullable=False)
    Position = db.Column(db.String(20), db.ForeignKey(Position.Zone), nullable=False)
    Date = db.Column(db.DateTime, nullable=False)
    Number_of_entrance = db.Column(db.Integer, nullable=False)
    Ticket_price = db.Column(db.Integer)
    Typology = db.Column(db.String(20))


class join_Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(100))
    Name = db.Column(db.String(20), nullable=False)
    Organiser = db.Column(db.String(20), nullable=False)
    Position = db.Column(db.String(20), db.ForeignKey(Position.Zone), nullable=False)
    Date = db.Column(db.DateTime, nullable=False)
    Number_of_entrance = db.Column(db.Integer, nullable=False)
    Ticket_price = db.Column(db.Integer)
    Typology = db.Column(db.String(20))


class Feedback(db.Model):
    No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Author = db.Column(db.String(20))
    Address = db.Column(db.String(20))
    Data = db.Column(db.Integer)
    Rate = db.Column(db.Integer)


class Host(db.Model):
    HostID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(20))
    Name = db.Column(db.String(20))
    Position = db.Column(db.String(20))
    Typology = db.Column(db.String(20))




db.create_all()
