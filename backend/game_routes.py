from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import socketio, db, emit
from models import Player, Game
from game_logic import BlackjackGame

game_routes = Blueprint('game_routes', __name__)
game_instance = BlackjackGame()  # Initialize game instance

@game_routes.route('/start_game', methods=['POST'])
@login_required
def start_game():
    user_id = current_user.id  # Get the id of the current logged-in user
    game_instance.start_game(user_id)  # Start game for user_id
    db.session.commit()  # Save all changes to the database
    return jsonify({'message': 'Game started'})

@socketio.on('hit')
@login_required
def handle_hit(data):
    user_id = current_user.id
    game_id = data.get('game_id')  # You may need to pass game_id from client
    game_instance.hit(user_id, game_id)  # Player hits
    db.session.commit()  # Commit changes to the database
    emit('game_state', {'game_data': game_instance.get_game_state(user_id)}, broadcast=True)

@socketio.on('stand')
@login_required
def handle_stand(data):
    user_id = current_user.id
    game_id = data.get('game_id')  # You may need to pass game_id from client
    game_instance.stand(user_id, game_id)  # Player stands
    db.session.commit()  # Commit changes to the database
    emit('game_state', {'game_data': game_instance.get_game_state(user_id)}, broadcast=True)

@game_routes.route('/double_down', methods=['POST'])
@login_required
def handle_double_down():
    user_id = current_user.id
    game_id = request.json.get('game_id')  # You may need to pass game_id from client
    game_instance.double_down(user_id, game_id)  # Player double downs
    db.session.commit()  # Commit changes to the database
    return jsonify({
        'hand': game_instance.get_player_hand(user_id, game_id),
        'double_down': game_instance.get_double_down_status(user_id, game_id)
    })

