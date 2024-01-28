import random
from .models import db, Game, Player

class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.shuffle_deck()

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks] * 4

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def start_game(self, user_id):
        # Ensure there is a shuffled deck for the game
        if len(self.deck) < 20:
            self.deck = self.create_deck()
            self.shuffle_deck()
        
        # Find or create a new game
        player = Player.query.filter_by(user_id=user_id).first()
        if not player:
            new_game = Game(game_state='active')
            db.session.add(new_game)
            db.session.commit()
            player_hand = [self.deck.pop(), self.deck.pop()]
            player = Player(user_id=user_id, game_id=new_game.id, hand=player_hand, credits=1000, bet=0)
            db.session.add(player)
        else:
            # Check if there's an active game
            new_game = Game.query.get(player.game_id)
            if not new_game or new_game.game_state != 'active':
                new_game = Game(game_state='active')
                db.session.add(new_game)
                db.session.commit()
                player.game_id = new_game.id

            # Reset the player's hand for a new round
            player.hand = [self.deck.pop(), self.deck.pop()]
            player.in_game = True

        db.session.commit()

    def deal_player_card(self, player_id, game_id):
        player = Player.query.filter_by(user_id=player_id, game_id=game_id).first()
        if player and player.in_game:
            player.hand.append(self.deck.pop())  # Add a card to the hand
            db.session.commit()  # Save changes

    def hit(self, player_id, game_id):
        player = Player.query.filter_by(user_id=player_id, game_id=game_id).first()
        if player and player.in_game:
            player.hand.append(self.deck.pop())
            if self.calculate_score(player.hand) > 21:
                player.in_game = False
            db.session.commit()

    def stand(self, player_id, game_id):
        player = Player.query.filter_by(user_id=player_id, game_id=game_id).first()
        if player:
            player.in_game = False  # Player stands, no more actions allowed
            db.session.commit()  # Save changes

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

    def determine_winner(self, player_id, game_id):
        player = Player.query.filter_by(user_id=player_id, game_id=game_id).first()
        dealer_score = self.calculate_score(player.game.dealer_hand)
        player_score = self.calculate_score(player.hand)
        if player_score > 21:
            return 'Lose'
        elif dealer_score > 21 or player_score > dealer_score:
            return 'Win'
        elif player_score == dealer_score:
            return 'Tie'
        else:
            return 'Lose'

    def place_bet(self, player_id, game_id, bet_amount):
        player = Player.query.filter_by(user_id=player_id, game_id=game_id).first()
        if player and player.credits >= bet_amount:
            player.bet += bet_amount
            player.credits -= bet_amount
            db.session.commit()

# Instantiate the game object
game_instance = BlackjackGame()


#    def double_down(self, player_id, game_id):
#        player = Player.query.filter_by(user_id=player_id, game_id=game_id).first()
#        if player and len(player.hand) == 2 and player.credits >= player.bet:
#            player.hand.append(self.deck.pop())  # Add a card to the hand
#            player.credits -= player.bet  # Deduct the bet amount from credits
#            player.bet *= 2  # Double the bet
#            player.in_game = False  # Player stands, no more actions allowed
#            db.session.commit()  # Save changes

#    def split_hand(self, player_id, game_id):
#        player = Player.query.filter_by(user_id=player_id, game_id=game_id).first()
#        # Split the hand and adjust bet and credits
#        if player and self.can_split(player.hand):
#            player.split_hand = [player.hand.pop()]
#            player.hand.append(self.deck.pop())
#            player.split_hand.append(self.deck.pop())
#            player.has_split = True
#            player.credits -= player.bet
#            player.bet *= 2
#            db.session.commit()

#    def can_split(self, hand):
#        return len(hand) == 2 and hand[0]['rank'] == hand[1]['rank']

