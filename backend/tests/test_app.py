import unittest
from backend.app import app, db
from backend.models import User, Game, Player, Leaderboard
from backend.game_logic import BlackjackGame

class BlackjackGameTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.game = BlackjackGame()

        # Create a test user
        test_user = User(username='testuser', password_hash='testpassword')
        db.session.add(test_user)
        db.session.commit()
        self.test_user_id = test_user.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_start_game(self):
        self.game.start_game(self.test_user_id)
        
        game = Game.query.join(Player).filter(Player.user_id == self.test_user_id).first()
        self.assertIsNotNone(game)
        self.assertEqual(game.game_state, 'active')

    def test_hit(self):
        self.game.start_game(self.test_user_id)
        game_id = Game.query.filter(Game.players.any(user_id=self.test_user_id)).first().id
        self.game.hit(self.test_user_id, game_id)
        player = Player.query.filter_by(user_id=self.test_user_id, game_id=game_id).first()
        self.assertGreater(len(player.hand), 2)

#    def test_double_down(self):
#        self.game.start_game(self.test_user_id)
#        game = Game.query.filter(Game.players.any(user_id=self.test_user_id)).first()
#        player = Player.query.filter_by(user_id=self.test_user_id, game_id=game.id).first()
#        initial_bet = 10
#        player.bet = initial_bet
#        player.credits = 1000
#        db.session.commit()

#        self.game.double_down(self.test_user_id, game.id)
#        db.session.refresh(player)

#        self.assertEqual(len(player.hand), 3)
#        self.assertEqual(player.bet, initial_bet * 2)
#        self.assertEqual(player.credits, 1000 - initial_bet)

#    def test_split_hand(self):
#        self.game.start_game(self.test_user_id)
#        game = Game.query.filter(Game.players.any(user_id=self.test_user_id)).first()
#        player = Player.query.filter_by(user_id=self.test_user_id, game_id=game.id).first()
#        player.hand = [{'rank': '8', 'suit': 'Hearts'}, {'rank': '8', 'suit': 'Diamonds'}]
#        player.credits = 1000
#        player.bet = 100
#        db.session.commit()

#        self.game.split_hand(self.test_user_id, game.id)
#        db.session.refresh(player)

#        self.assertEqual(len(player.hand), 1)  # After split, one card should remain in the original hand
#        self.assertTrue(player.has_split)  # `has_split` should be True
#        self.assertEqual(len(player.split_hand), 1)  # One card should be in the split hand
#        self.assertEqual(player.credits, 900)  # Credits should be reduced by the bet amount
#        self.assertEqual(player.bet, 200)  # Bet should be doubled

if __name__ == '__main__':
    unittest.main()

