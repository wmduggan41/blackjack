from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user
from werkzeug.security import check_password_hash
from .auth import auth_blueprint
from .models import db, User
from .game_logic import BlackjackGame

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hombresride4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blackjack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# Initialize Flask extensions
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Unittest configuration
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # or another URI for your test database
    # ... other test-specific configurations


# Blueprint for authentication routes
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login route
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify(message='Logged in successfully'), 200
    return jsonify(message='Invalid username or password'), 401

@app.route('/new_game', methods=['GET', 'POST'])  # Use the correct method
def new_game():
    # Logic for starting a new game
    return jsonify({'message': 'New game started'}), 200

# SocketIO events
@socketio.on('join_game')
def handle_join_game(data):
    # Handle join game logic
    pass

@socketio.on('new_game')
def handle_new_game():
    # Logic to create a new game
    pass

@socketio.on('player_action')
def handle_player_action(data):
    action = data['action']
    # Logic based on the action (hit, stand, double_down)
    pass

@socketio.on('place_bet')
def handle_place_bet(data):
    bet_amount = data['betAmount']
    # Logic to handle the bet
    pass

# Run Flask app with SocketIO
if __name__ == '__main__':
    socketio.run(app, debug=True)


