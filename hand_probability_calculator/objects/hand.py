from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property, reduce
from itertools import chain
from operator import mul

from scipy.special import comb

from .hand_component import HandComponent


@dataclass
class Hand:
    hand_components: list[HandComponent]
    tier: int = None
    tier_distance: dict = field(default_factory=lambda: defaultdict(dict))
    tierwise_lacking_cards: dict = field(default_factory=lambda: defaultdict(dict))
    tierup_possibility: dict = field(default_factory=lambda: defaultdict(float))

    @cached_property
    def cards(self) -> tuple[str]:
        return tuple(chain.from_iterable(component.explode() for component in self.hand_components))

    @cached_property
    def n_cards_can_draw(self):
        if "金満で謙虚な壺" in set(self.cards):
            return 1
        else:
            return 0

    @cached_property
    def is_possible_to_improve_tier(self):
        return any([self.n_cards_can_draw >= distance for distance in self.tier_distance.values()])

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
        dic = {
            "cards": self.cards,
            "tier": self.tier,
            "hand_trap_score": self.hand_trap_score,
            "hand_trap_defence_score": self.hand_trap_defence_score,
            "n_combinations": self.n_combinations,
        }
        dic.update(self._probability_to_dict())
        return dic

    def _probability_to_dict(self):
        if not self.is_possible_to_improve_tier:
            return {f"tier_{self.tier}_probability": 1}

        prob_dict = {f"tier_{tier}_probability": possibility for tier, possibility in self.tierup_possibility.items()}
        prob_dict[f"tier_{self.tier}_probability"] = 1 - sum(prob_dict.values())
        return prob_dict
