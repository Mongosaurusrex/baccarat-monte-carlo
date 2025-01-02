import random
from typing import List


class Card:
    def __init__(self, value, suit) -> None:
        self.value = value
        self.suit = suit

    def __repr__(self) -> str:
        return f"{self.value} {self.suit}"


class DeckFactory:
    def __init__(self, num_decks=6) -> None:
        self.num_decks = num_decks
        self.cards: List[Card] = []

        self.values = list(range(2, 15))
        self.suits = ["clubs", "diamonds", "spades", "hearts"]
        self.face_cards = {
            11: "J",
            12: "Q",
            13: "K",
            14: "A",
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }

        self._create_shuffled_deck()

    def draw_card(self) -> Card:
        if len(self.cards) == 0:
            self._create_shuffled_deck()

        return self.cards.pop()

    def _create_shuffled_deck(self) -> None:
        for _ in range(self.num_decks):
            for value in self.values:
                for suit in self.suits:
                    if value in self.face_cards:
                        card_value = self.face_cards[value]
                        self.cards.append(Card(card_value, suit))
                    else:
                        self.cards.append(Card(value, suit))

        random.shuffle(self.cards)
