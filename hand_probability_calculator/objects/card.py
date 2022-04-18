from dataclasses import dataclass, field

import numpy as np


@dataclass
class Card:
    id: int
    name: str
    deck_amount: int
    tags: set[str]
    onehot_vector: np.array = field(repr=False)
