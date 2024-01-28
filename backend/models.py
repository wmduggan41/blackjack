from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()  # db is initialized in app.py and imported here

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # Store hashed passwords

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dealer_hand = db.Column(db.PickleType)  # Stores a list of card dictionaries
    game_state = db.Column(db.String(50), default='active')  # 'active', 'finished', etc.
    players = db.relationship('Player', backref='game', lazy='dynamic')

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    hand = db.Column(db.PickleType)  # Stores a list of card dictionaries
    split_hand = db.Column(db.PickleType, nullable=True)  # Stores a list of card dictionaries for the split hand
    bet = db.Column(db.Float, default=0.0)  # The current bet for the round
    credits = db.Column(db.Float, default=1000.0)  # The player's available credits
    has_split = db.Column(db.Boolean, default=False)  # If the player has split their hand
    in_game = db.Column(db.Boolean, default=True)  # If the player is still in the game this round

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_winnings = db.Column(db.Float)  # The total winnings for the user
    date = db.Column(db.DateTime, default=datetime.utcnow)  # The date when the record was created or updated

