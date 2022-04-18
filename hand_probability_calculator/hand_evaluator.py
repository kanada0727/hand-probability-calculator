import numpy as np
import pandas as pd

from hand_probability_calculator.possible_hand_enumerator import PossibleHandEnumerator


class HandEvaluator:
    @classmethod
    def run(cls, deck, hand_conditions):
        hands = PossibleHandEnumerator.run(deck)
        cond_vectors = cls._vectorize_conditions(hand_conditions)
        for hand in hands:
            hand.tier = cls._evaluate_hand(hand, cond_vectors)
        return pd.DataFrame.from_records([hand.to_dict() for hand in hands])

    @staticmethod
    def _vectorize_conditions(conditions):
        vectors = dict()
        for tier in conditions.tiers:
            vectors[tier] = np.vstack([x.vector for x in conditions.query(f"tier == {tier}")])
        return vectors

    @staticmethod
    def _evaluate_hand(hand, cond_vectors):
        for tier, vector in cond_vectors.items():
            if any((vector - hand.vector).clip(0).sum(axis=1) == 0):
                return tier
        return -1
