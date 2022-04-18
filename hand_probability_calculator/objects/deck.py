from dataclasses import dataclass
from functools import cached_property

import pandas as pd
import numpy as np

from .card import Card


@dataclass
class Deck:
    cards: list[Card]

    def __post_init__(self):
        self._df = pd.DataFrame(self.cards)
        self._flatten_df = self._flatten_cards(self.cards)
        self.cards = pd.Series(self.cards)

    @staticmethod
    def _flatten_cards(cards):
        return pd.DataFrame(cards).explode("tags").rename({"tags": "tag"}, axis=1)

    def __repr__(self):
        return self._df.__repr__()

    @classmethod
    def load_csv(cls, fname):
        return Deck(CsvDeckReader.run(fname))

    def query(self, query_str):
        return self.cards[self._flatten_df.query(query_str).index.drop_duplicates()]

    @cached_property
    def total_amount(self):
        return sum([card.deck_amount for card in self.cards])

    @cached_property
    def total_variation(self):
        return len(self.cards)


class CsvDeckReader:
    @classmethod
    def run(cls, fname):
        card_list = pd.read_csv(fname)
        card_list["id"] = card_list.index
        card_list["tags"] = card_list.tags.map(cls._parse_tag)
        card_list["onehot_vector"] = list(np.eye(len(card_list)))
        return card_list.apply(lambda card: Card(**card.to_dict()), axis=1).values.tolist()

    @staticmethod
    def _parse_tag(tags):
        return set(tag.strip() for tag in tags.split(","))
