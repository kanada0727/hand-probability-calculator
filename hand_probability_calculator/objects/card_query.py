from dataclasses import dataclass
from itertools import chain


@dataclass
class CardQuery:
    conditions: list[dict]

    def apply(self, deck):
        return deck.query(self._build_query())

    def _build_query(self):
        return " or ".join(
            chain.from_iterable(
                [
                    [self._build_single_query_string(key, value) for key, value in condition.items()]
                    for condition in self.conditions
                ]
            )
        )

    @classmethod
    def _build_single_query_string(cls, key, value):
        return f"{key} == '{value}'"
