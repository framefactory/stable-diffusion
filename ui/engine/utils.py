from inspect import getmembers, isroutine
from copy import copy, deepcopy
from datetime import datetime

class DataClass:
    def to_dict(self) -> dict:
        attribs = getmembers(self, lambda a: not isroutine(a))
        attribs = [ a for a in attribs if not a[0].startswith("__") ]
        return deepcopy(dict(attribs))


def generate_file_name_now(ext: str = "") -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3] + ext
