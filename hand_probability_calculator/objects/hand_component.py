from dataclasses import dataclass
from functools import cached_property

from .card import Card


@dataclass
class HandComponent:
    card: Card
    hand_amount: int

    def explode(self):
        return tuple([self.card.name]) * self.hand_amount

    @cached_property
    def vector(self):
        return self.card.onehot_vector * self.hand_amount

    @cached_property
    def hand_trap_score(self):
        if "誘発" not in self.card.tags:
            return 0
        if "ターン1" in self.card.tags:
            return 1
        return self.hand_amount

    @cached_property
    def hand_trap_defence_score(self):
        if "誘発防御" not in self.card.tags:
            return 0
        if "ターン1" in self.card.tags:
            return 1
        return self.hand_amount
