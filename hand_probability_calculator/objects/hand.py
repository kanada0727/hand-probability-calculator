from dataclasses import dataclass
from functools import cached_property, reduce
from itertools import chain
from operator import mul

from scipy.special import comb

from .hand_component import HandComponent


@dataclass
class Hand:
    hand_components: list[HandComponent]
    tier: int = None

    @cached_property
    def cards(self) -> tuple[str]:
        return tuple(chain.from_iterable(component.explode() for component in self.hand_components))

    @cached_property
    def is_valid(self) -> bool:
        """
        同一カード名のcomponentがcombinationに複数含まれている場合invalid
        """
        return len(self.hand_components) == len(set(component.card.name for component in self.hand_components))

    @cached_property
    def vector(self):
        return sum([component.vector for component in self.hand_components])

    @cached_property
    def n_combinations(self):
        return reduce(
            mul,
            [
                comb(
                    hand_component.card.deck_amount,
                    hand_component.hand_amount,
                    exact=True,
                )
                for hand_component in self.hand_components
            ],
        )

    @cached_property
    def hand_trap_score(self):
        # hand_trap_score = 1ターンに使える誘発枚数
        return sum([component.hand_trap_score for component in self.hand_components])

    @cached_property
    def hand_trap_defence_score(self):
        # hand_trap_defence_score = 相手の誘発に対する妨害枚数
        return sum([component.hand_trap_defence_score for component in self.hand_components])

    def __repr__(self):
        return "Hand" + str(self.cards)

    def to_dict(self):
        return {
            "cards": self.cards,
            "tier": self.tier,
            "hand_trap_score": self.hand_trap_score,
            "hand_trap_defence_score": self.hand_trap_defence_score,
            "n_combinations": self.n_combinations,
        }
