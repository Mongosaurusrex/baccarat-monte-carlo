import unittest
from utils.deck import DeckFactory, Card

class TestDeckFactory(unittest.TestCase):
    def setUp(self):
        self.deck_factory = DeckFactory(num_decks=1)

    def test_deck_initialization(self):
        self.assertEqual(len(self.deck_factory.cards), 52)

        valid_values = list(range(2, 11)) + ["J", "Q", "K", "A"]
        valid_suits = ["clubs", "diamonds", "spades", "hearts"]

        for card in self.deck_factory.cards:
            self.assertIn(card.value, valid_values)
            self.assertIn(card.suit, valid_suits)

    def test_draw_card(self):
        initial_count = len(self.deck_factory.cards)
        card = self.deck_factory.draw_card()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(self.deck_factory.cards), initial_count - 1)

    def test_deck_reshuffle_when_empty(self):
        for _ in range(len(self.deck_factory.cards)):
            self.deck_factory.draw_card()

        self.assertEqual(len(self.deck_factory.cards), 0)

        card = self.deck_factory.draw_card()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(self.deck_factory.cards), 51)

    def test_no_duplicates_after_shuffle(self):
        cards_seen = set()
        for card in self.deck_factory.cards:
            self.assertNotIn((card.value, card.suit), cards_seen)
            cards_seen.add((card.value, card.suit))

    def test_multiple_decks(self):
        multi_deck_factory = DeckFactory(num_decks=2)
        self.assertEqual(len(multi_deck_factory.cards), 104)

    def test_card_string_representation(self):
        card = Card("A", "hearts")
        self.assertEqual(repr(card), "A hearts")

if __name__ == "__main__":
    unittest.main()
