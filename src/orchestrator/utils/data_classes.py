from dataclasses import dataclass
from typing import Union


@dataclass
class SavedItem:
    identifier: Union[str, int]
