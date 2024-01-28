import random

class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.players = {}  # Keyed by player_id

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks] * 4

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def start_game(self, player_id):
        if len(self.deck) < 20:
            self.deck = self.create_deck()
            self.shuffle_deck()

        self.players[player_id] = {
            'hand': [self.deck.pop(), self.deck.pop()],
            'in_game': True,
            'bet': 0,
            'credits': 1000,  # Example starting credit
            'split_hand': None,
            'has_split': False
        }

    def hit(self, player_id):
        player = self.players.get(player_id)
        if player and player['in_game']:
            player['hand'].append(self.deck.pop())
            if self.calculate_score(player['hand']) > 21:
                player['in_game'] = False

    def stand(self, player_id):
        player = self.players.get(player_id)
        if player:
            player['in_game'] = False

    def double_down(self, player_id):
        player = self.players.get(player_id)
        if player and len(player['hand']) == 2 and player['credits'] >= player['bet']:
            player['hand'].append(self.deck.pop())
            player['credits'] -= player['bet']
            player['bet'] *= 2
            player['in_game'] = False

    def split_hand(self, player_id):
        player = self.players.get(player_id)
        if player and self.can_split(player['hand']):
            player['split_hand'] = [player['hand'].pop()]
            player['has_split'] = True
            player['hand'].append(self.deck.pop())
            player['split_hand'].append(self.deck.pop())

    def can_split(self, hand):
        return len(hand) == 2 and hand[0]['rank'] == hand[1]['rank']

    def calculate_score(self, hand):
        score = 0
        ace_count = 0
        for card in hand:
            if card['rank'] in ['J', 'Q', 'K']:
                score += 10
            elif card['rank'] == 'A':
                ace_count += 1
                score += 11
            else:
                score += int(card['rank'])
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1
        return score

    def determine_winner(self, player_id):
        player = self.players.get(player_id)
        dealer_score = self.calculate_score(self.players['dealer']['hand'])
        player_score = self.calculate_score(player['hand'])
        if player_score > 21:
            return 'Lose'
        elif dealer_score > 21 or player_score > dealer_score:
            return 'Win'
        elif player_score == dealer_score:
            return 'Tie'
        else:
            return 'Lose'

    def place_bet(self, player_id, bet_amount):
        player = self.players.get(player_id)
        if player and player['credits'] >= bet_amount:
            player['bet'] = bet_amount
            player['credits'] -= bet_amount

    # Add additional methods needed for the game logic

# Instantiate the game object
game_instance = BlackjackGame()
