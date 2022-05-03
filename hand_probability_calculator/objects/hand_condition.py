from dataclasses import dataclass, field
from itertools import product

import numpy as np

from .card import Card
from .card_condition import CardCondition
from .deck import Deck


@dataclass
class HandCondition:
    n_hands: int
    tier: int
    combination: dict
    deck: Deck = field(repr=False)

    def __post_init__(self):
        self.combination_factors = [
            self.deck.query(str(CardCondition(condition))) for condition in self.combination.values()
        ]
        self.card_combinations = [HandConditionSample(cards) for cards in product(*self.combination_factors)]
        self.vector = np.vstack([card_combination.vector for card_combination in self.card_combinations])


@dataclass
class HandConditionSample:
    cards: list[Card]

    def __post_init__(self):
        self.vector = sum(card.onehot_vector for card in self.cards)

    def __repr__(self):
        return "HandConditionSample" + str(tuple(card.name for card in self.cards))
