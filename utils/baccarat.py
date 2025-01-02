from dataclasses import dataclass
from typing import List
from utils.deck import Card, DeckFactory


@dataclass
class RoundHistoryItem:
    bet_choice: str
    winner: str
    funds: float
    bank_hand: List[Card]
    player_hand: List[Card]
    went_bankrupt: bool


class Game:
    def __init__(
        self,
        starting_money: int,
        betting_amount: int,
        betting_pattern: List[str],
        max_simulations: int = 1000,
    ) -> None:
        self.funds = starting_money
        self.initial_bet = betting_amount
        self.current_bet = betting_amount
        self.betting_pattern = betting_pattern
        self.max_simulations = max_simulations
        self.bankrupt = False
        self.deck_factory = DeckFactory()
        self.finished_simulation = False
        self.history: List[RoundHistoryItem] = []
        self.pattern_index = 0
        self.last_result = None

    def get_next_bet(self) -> str:
        if self.last_result == "win":
            self.pattern_index = 0
            self.current_bet = self.initial_bet
        elif self.last_result == "loss":
            self.pattern_index = (self.pattern_index + 1) % len(self.betting_pattern)
            self.current_bet *= 2

        self.current_bet = min(self.current_bet, self.funds)

        return self.betting_pattern[self.pattern_index]

    def determine_winner(self, bank_hand: List[Card], player_hand: List[Card]) -> str:
        hand_total = (
            lambda hand: sum(
                card.value if isinstance(card.value, int) else 10 for card in hand
            )
            % 10
        )

        player_total = hand_total(player_hand)
        bank_total = hand_total(bank_hand)

        if player_total in [8, 9] or bank_total in [8, 9]:
            return "Player" if player_total > bank_total else "Banker"

        if len(player_hand) == 2 and player_total <= 5:
            player_hand.append(self.deck_factory.draw_card())
            player_total = hand_total(player_hand)

        if len(bank_hand) == 2:
            if len(player_hand) == 2:
                if bank_total <= 5:
                    bank_hand.append(self.deck_factory.draw_card())
                    bank_total = hand_total(bank_hand)
        else:
            player_third_card = player_hand[2].value if len(player_hand) > 2 else None

            if bank_total <= 2:
                bank_hand.append(self.deck_factory.draw_card())
            elif bank_total == 3 and player_third_card != 8:
                bank_hand.append(self.deck_factory.draw_card())
            elif bank_total == 4 and player_third_card in range(2, 8):
                bank_hand.append(self.deck_factory.draw_card())
            elif bank_total == 5 and player_third_card in range(4, 8):
                bank_hand.append(self.deck_factory.draw_card())
            elif bank_total == 6 and player_third_card in range(6, 8):
                bank_hand.append(self.deck_factory.draw_card())

            if len(bank_hand) > 2:
                bank_total = hand_total(bank_hand)

        if player_total > bank_total:
            return "Player"
        elif bank_total > player_total:
            return "Banker"
        else:
            return "Tie"

    def calculate_funds_change(self, winner: str, bet_choice: str):
        if winner == bet_choice:
            self.funds += self.current_bet
            self.last_result = "win"
        elif winner == "Tie":
            self.last_result = "tie"
        else:
            self.funds -= self.current_bet
            self.last_result = "loss"

        if self.funds <= 0:
            self.bankrupt = True

    def play_round(self) -> None:
        bet_choice = self.get_next_bet()
        bank_hand = [self.deck_factory.draw_card(), self.deck_factory.draw_card()]
        player_hand = [self.deck_factory.draw_card(), self.deck_factory.draw_card()]

        winner = self.determine_winner(bank_hand=bank_hand, player_hand=player_hand)
        self.calculate_funds_change(winner=winner, bet_choice=bet_choice)

        self.history.append(
            RoundHistoryItem(
                bet_choice=bet_choice,
                winner=winner,
                funds=self.funds,
                bank_hand=bank_hand,
                player_hand=player_hand,
                went_bankrupt=self.bankrupt,
            )
        )

    def simulate(self) -> List[RoundHistoryItem]:
        for _ in range(self.max_simulations):
            if self.bankrupt:
                break
            self.play_round()

        return self.history
