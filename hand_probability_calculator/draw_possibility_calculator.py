from scipy.special import comb


class DrawPossibilityCalculator:
    @classmethod
    def run(cls, hand, deck):
        rest_of_deck = deck.vector - hand.vector
        tierwise_lacking_cards = cls._reshape_lacking_cards(hand.tierwise_lacking_cards)

        tierwise_draw_possibility = cls._calc_tierwise_draw_possibility(rest_of_deck, tierwise_lacking_cards)
        return tierwise_draw_possibility

    def _reshape_lacking_cards(lacking_cards):
        reshaped = dict()
        listed_cards = set()
        for key, cards_onehot in lacking_cards.items():
            card_indices = set(cards_onehot.argmax(axis=-1)) - listed_cards
            reshaped[key] = list(card_indices)
            listed_cards |= card_indices
        return reshaped

    @classmethod
    def _calc_tierwise_draw_possibility(cls, rest_of_deck, tierwise_lacking_cards):
        tierwise_lacking_card_amounts = {
            tier: rest_of_deck[cards].sum() for tier, cards in tierwise_lacking_cards.items()
        }
        rest_of_deck_amount = rest_of_deck.sum()
        nontarget_card_amount = rest_of_deck_amount - sum(tierwise_lacking_card_amounts.values())

        considered_card_amount = nontarget_card_amount
        tierwise_draw_possibility = dict()

        for tier in sorted(tierwise_lacking_card_amounts.keys(), reverse=True):
            tierwise_draw_possibility[tier] = cls._calc_specific_tier_possibility(
                considered_card_amount,
                tierwise_lacking_card_amounts[tier],
                rest_of_deck_amount,
            )
            considered_card_amount += tierwise_lacking_card_amounts[tier]

        return tierwise_draw_possibility

    def _calc_specific_tier_possibility(considered_card_amount, lacking_card_amount, rest_of_deck_amount, n_excavate=6):
        """
        tierごとにめくりたいカードの増分を考慮してめくる確率を算出する
        """
        return (
            comb(considered_card_amount + lacking_card_amount, n_excavate, exact=True)
            - comb(considered_card_amount, n_excavate, exact=True)
        ) / comb(rest_of_deck_amount, n_excavate, exact=True)
