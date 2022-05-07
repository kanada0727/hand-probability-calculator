from itertools import chain, combinations, product

from hand_probability_calculator.objects.hand import Hand
from objects.hand_component import HandComponent


class PossibleHandEnumerator:
    AMOUNT_COMBINATIONS = [
        {3: 1, 2: 1},
        {3: 1, 1: 2},
        {2: 2, 1: 1},
        {2: 1, 1: 3},
        {1: 5},
    ]

    @classmethod
    def run(cls, deck):
        return list(
            chain.from_iterable(
                cls._enumerate_for_specific_amount_combination(deck, amount_combination)
                for amount_combination in cls.AMOUNT_COMBINATIONS
            )
        )

    @classmethod
    def _enumerate_for_specific_amount_combination(cls, deck, amount_combination):
        hand_components = []

        for hand_amount, n_elements in amount_combination.items():
            hand_components.append(cls._enumerate_for_specific_amount_elements(deck, hand_amount, n_elements))

        hands = [Hand(tuple(chain.from_iterable(x))) for x in list(product(*hand_components))]
        hands = [hand for hand in hands if cls._is_valid_hand(hand)]

        return hands

    @staticmethod
    def _is_valid_hand(hand: Hand) -> bool:
        """
        同一カード名のcomponentがcombinationに複数含まれている場合invalid
        """
        return len(hand.hand_components) == len(set(component.card.name for component in hand.hand_components))

    @staticmethod
    def _enumerate_for_specific_amount_elements(deck, hand_amount, n_elements):
        candidates = deck.query(f"deck_amount >={hand_amount}").map(
            lambda card: HandComponent(
                hand_amount=hand_amount,
                card=card,
            )
        )
        return combinations(candidates, n_elements)
