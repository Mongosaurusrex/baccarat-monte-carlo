import unittest
from utils.deck import Card, DeckFactory
from utils.baccarat import Game, RoundHistoryItem


class TestBaccaratGame(unittest.TestCase):
    def setUp(self):
        self.betting_pattern = ["Player", "Banker", "Tie"]
        self.game = Game(
            starting_money=1000,
            betting_amount=10,
            betting_pattern=self.betting_pattern,
            max_simulations=100,
        )

    def test_initialization(self):
        self.assertEqual(self.game.funds, 1000)
        self.assertEqual(self.game.current_bet, 10)
        self.assertEqual(self.game.initial_bet, 10)
        self.assertEqual(self.game.betting_pattern, ["Player", "Banker", "Tie"])
        self.assertEqual(self.game.pattern_index, 0)
        self.assertFalse(self.game.bankrupt)

    def test_betting_logic_win(self):
        self.game.last_result = "win"
        bet_choice = self.game.get_next_bet()
        self.assertEqual(bet_choice, "Player")
        self.assertEqual(self.game.current_bet, 10)
        self.assertEqual(self.game.pattern_index, 0)

    def test_betting_logic_loss(self):
        self.game.last_result = "loss"
        bet_choice = self.game.get_next_bet()
        self.assertEqual(bet_choice, "Banker")
        self.assertEqual(self.game.current_bet, 20)
        self.assertEqual(self.game.pattern_index, 1)

    def test_betting_logic_tie(self):
        self.game.last_result = "tie"
        self.game.pattern_index = 1
        self.game.current_bet = 40
        bet_choice = self.game.get_next_bet()
        self.assertEqual(bet_choice, "Banker")
        self.assertEqual(self.game.current_bet, 40)

    def test_bet_cannot_exceed_funds(self):
        self.game.funds = 50
        self.game.last_result = "loss"
        bet_choice = self.game.get_next_bet()
        self.assertEqual(self.game.current_bet, 20)

    def test_bankruptcy(self):
        self.game.funds = 10
        self.game.current_bet = 20
        self.game.play_round()
        self.assertTrue(self.game.bankrupt)
        self.assertEqual(self.game.funds, 0)

    def test_round_history(self):
        self.game.play_round()
        self.assertGreater(len(self.game.history), 0)
        round_item = self.game.history[0]
        self.assertIsInstance(round_item, RoundHistoryItem)
        self.assertIn(round_item.winner, ["Player", "Banker", "Tie"])
        self.assertGreaterEqual(round_item.funds, 0)

    def test_simulation(self):
        history = self.game.simulate()
        self.assertLessEqual(len(history), 100)
        if self.game.bankrupt:
            self.assertEqual(self.game.funds, 0)
        else:
            self.assertGreater(self.game.funds, 0)

    def test_tie_scenario(self):
        self.game.last_result = "tie"
        self.game.current_bet = 10
        self.game.pattern_index = 0
        self.game.play_round()
        self.assertEqual(self.game.current_bet, 10)
        self.assertEqual(self.game.pattern_index, 0)

    def test_loss_streak(self):
        self.game.funds = 100
        for _ in range(10):
            self.game.last_result = "loss"
            self.game.play_round()
            if self.game.bankrupt:
                break
        self.assertTrue(self.game.bankrupt)


if __name__ == "__main__":
    unittest.main()
