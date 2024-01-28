from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()  # Assuming db is initialized in app.py and imported here

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # Store hashed passwords

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dealer_hand = db.Column(db.PickleType)  # Store dealer hand as a list of cards
    game_state = db.Column(db.String(50), default='active') # Store game state e.g., "active"
    players = db.relationship('Player', backref='game')

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    hand = db.Column(db.PickleType)  # Storing hand as a pickled object
    bet = db.Column(db.Float)  # Current bet
    credits = db.Column(db.Float)  # Current credits in USD
    has_split = db.Column(db.Boolean, default=False)  # If the player has chosen to split

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_winnings = db.Column(db.Float) # Total USD value won
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

