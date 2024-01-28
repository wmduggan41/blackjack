from flask import Flask, jsonify, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from models import db, User, Game, Player
from game_logic import BlackjackGame

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hombresride4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blackjack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)

game_instance = BlackjackGame()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify(message='Logged in successfully'), 200
    return jsonify(message='Invalid username or password'), 401

@app.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(message='Logged out successfully'), 200

@app.route('/game/new_game', methods=['POST'])
@login_required
def new_game_route():
    game_instance.start_game(current_user.id)
    db.session.commit()
    return jsonify(message='New game started'), 200

@socketio.on('join_game')
@login_required
def on_join_game(data):
    room = data['room']
    join_room(room)
    emit('join_game', {'message': f'{current_user.username} has joined the game.'}, to=room)

@socketio.on('new_game')
@login_required
def on_new_game():
    game_instance.start_game(current_user.id)
    db.session.commit()
    emit('new_game', {'message': 'New game created.'}, broadcast=True)

@socketio.on('player_action')
@login_required
def on_player_action(data):
    action = data['action']
    game_id = data['game_id']
    if action == 'hit':
        game_instance.hit(current_user.id, game_id)
    elif action == 'stand':
        game_instance.stand(current_user.id, game_id)
    elif action == 'double_down':
        game_instance.double_down(current_user.id, game_id)
    db.session.commit()
    emit('player_action', {'action': action, 'game_data': game_instance.get_game_state(current_user.id)}, broadcast=True)

@socketio.on('place_bet')
@login_required
def on_place_bet(data):
    game_id = data['game_id']
    bet_amount = data['betAmount']
    game_instance.place_bet(current_user.id, game_id, bet_amount)
    db.session.commit()
    emit('place_bet', {'betAmount': bet_amount, 'game_data': game_instance.get_game_state(current_user.id)}, broadcast=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database is created
    socketio.run(app, debug=True)
