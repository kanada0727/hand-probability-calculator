from dataclasses import dataclass
from functools import cached_property

import pandas as pd
import yaml

from .hand_condition import HandCondition


@dataclass
class HandConditions:
    conditions: list[HandCondition]

    def __post_init__(self):
        self._df = pd.DataFrame(self.conditions)
        self.conditions = pd.Series(self.conditions)

    def query(self, query_str):
        return self.conditions[self._df.query(query_str).index]

    @cached_property
    def tiers(self):
        return self._df.tier.drop_duplicates().tolist()

    @classmethod
    def load_yaml(cls, fname, deck):
        conditions = YamlHandConditionReader.read(fname)
        conditions = conditions.apply(
            lambda condition: HandCondition(**condition.to_dict(), deck=deck), axis=1
        ).tolist()
        return HandConditions(conditions)

    def __getitem__(self, idx):
        return self.conditions[idx]

    def __repr__(self):
        return str(self._df)


class YamlHandConditionReader:
    @classmethod
    def read(cls, fname):
        return (
            pd.DataFrame(yaml.safe_load(open(fname)))
            .explode("combinations")
            .rename({"combinations": "combination"}, axis=1)
            .reset_index(drop=True)
        )
