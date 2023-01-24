from typing import Dict
from utils import SavedItem


class Repository:
    def save(self, data) -> SavedItem:
        raise NotImplementedError

    def get(self, uuid: str) -> Dict:
        raise NotImplementedError

    def update(self, uuid: str, data: Dict) -> Dict:
        raise NotImplementedError
