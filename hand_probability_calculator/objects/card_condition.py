from dataclasses import dataclass
from typing import Union


@dataclass
class ConditionBase:
    """
    カードの絞り込み条件
    single keyのdictで初期化される
    Example:
        {"name": "ナーベル"}
        {"or": [{"name": "ナーベル"}, {"monster_type": "獣族"}]}
    """

    condition: dict[str, Union[str, list[dict]]]

    def __post_init__(self):
        self.key = list(self.condition.keys())[0]
        self.value = list(self.condition.values())[0]

    def __str__(self):
        raise NotImplementedError


class CardCondition(ConditionBase):
    def __str__(self):
        if self.key == "and":
            return str(AndCondition(self.value))
        elif self.key == "or":
            return str(OrCondition(self.value))
        else:
            return str(SingleCondition(self.condition))


class SingleCondition(ConditionBase):
    def __str__(self):
        if self.key == "level":
            return f"{self.key} {self.value}"
        elif isinstance(self.value, list):
            return f"{self.key} in {self._convert_list_value(self.value)}"
        else:
            return f"{self.key} == {self._convert_value(self.value)}"

    @classmethod
    def _convert_list_value(cls, value):
        return f"[{','.join([cls._convert_value(v) for v in value])}]"

    @staticmethod
    def _convert_value(value):
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, int):
            return value


@dataclass
class AndCondition:
    conditions: list[dict]

    def __str__(self):
        return " and ".join(f"( {CardCondition(cond)} )" for cond in self.conditions)


@dataclass
class OrCondition:
    conditions: list[dict]

    def __str__(self):
        return " or ".join(f"( {CardCondition(cond)} )" for cond in self.conditions)
