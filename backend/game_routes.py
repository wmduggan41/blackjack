from flask import Blueprint, jsonify, request
from flask_socketio import emit
from app import socketio, game_instance  # Import game_instance from your game logic module

game_routes = Blueprint('game_routes', __name__)

@game_routes.route('/start_game', methods=['POST'])
def start_game():
    user_id = request.json.get('user_id')
    game_instance.start_game(user_id)  # Pass user_id to start_game
    return jsonify({'message': 'Game started'})

@socketio.on('hit')
def handle_hit(data):
    user_id = data['user_id']
    game_instance.hit(user_id)  # Update game state
    emit('game_state', {'game_data': game_instance.get_game_state(user_id)}, broadcast=True)

@socketio.on('stand')
def handle_stand(data):
    user_id = data['user_id']
    game_instance.stand(user_id)  # Update game state
    emit('game_state', {'game_data': game_instance.get_game_state(user_id)}, broadcast=True)

@game_routes.route('/double_down', methods=['POST'])
def handle_double_down():
    user_id = request.json.get('user_id')
    game_instance.double_down(user_id) # Update game state
    return jsonify({
        'hand': game_instance.players[user_id]['hand'],
        'double_down': game_instance.players[user_id]['double_down']
    })


