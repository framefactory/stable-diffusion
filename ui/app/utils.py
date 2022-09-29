from inspect import getmembers, isroutine
from copy import deepcopy
from datetime import datetime
import random

import numpy as np


class DataClass:
    def to_dict(self) -> dict:
        attribs = getmembers(self, lambda a: not isroutine(a))
        attribs = [ a for a in attribs if not a[0].startswith("__") ]
        return deepcopy(dict(attribs))


def generate_random_seed() -> int:
    random.seed()
    return random.randrange(0, np.iinfo(np.int32).max)