import numpy as np
import pandas as pd

from hand_probability_calculator.draw_possibility_calculator import DrawPossibilityCalculator
from hand_probability_calculator.possible_hand_enumerator import PossibleHandEnumerator


class HandEvaluator:
    @classmethod
    def run(cls, deck, hand_conditions):
        hands = PossibleHandEnumerator.run(deck)
        cond_vectors = cls._vectorize_conditions(hand_conditions)
        for hand in hands:
            hand = cls._evaluate_hand(hand, cond_vectors)
            if hand.is_possible_to_improve_tier:
                hand.tierup_possibility = DrawPossibilityCalculator.run(hand, deck)

        return pd.DataFrame.from_records([hand.to_dict() for hand in hands]).fillna(0)

    @staticmethod
    def _vectorize_conditions(conditions):
        vectors = dict()
        for tier in conditions.tiers:
            vectors[tier] = np.vstack([x.vector for x in conditions.query(f"tier == {tier}")])
        return vectors

    @staticmethod
    def _evaluate_hand(hand, cond_vectors):
        for tier, vector in cond_vectors.items():
            samplewise_tier_difference = (vector - hand.vector).clip(0)
            samplewise_tier_distance = samplewise_tier_difference.sum(axis=1)
            tier_distance = samplewise_tier_distance.min()

            if tier_distance == 0:
                hand.tier = tier
                return hand

            hand.tier_distance[tier] = tier_distance

            if tier_distance <= hand.n_cards_can_draw:
                hand.tierwise_lacking_cards[tier] = samplewise_tier_difference[
                    np.where(samplewise_tier_distance <= hand.n_cards_can_draw)
                ]

        hand.tier = -1
        return hand
