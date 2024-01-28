from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy() # db is initialized in app.py and imported here

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # Store hashed passwords

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dealer_hand = db.Column(db.PickleType)
    game_state = db.Column(db.String(50), default='active')
    players = db.relationship('Player', backref='game', lazy='dynamic')

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    hand = db.Column(db.PickleType)
    bet = db.Column(db.Float)
    credits = db.Column(db.Float)
    has_split = db.Column(db.Boolean, default=False)

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_winnings = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

