from typing import Dict, List, Union


class IRepository:
    model: str

    def __init__(self, model: str):
        self.model = model

    def get(self, uuid: str) -> Dict:
        raise NotImplementedError

    def save(self, data) -> Dict:
        raise NotImplementedError

    def update(self, uuid: str, data: Dict) -> Dict:
        raise NotImplementedError

    def search(self, filter: List[Union[str, List]]) -> Dict:
        raise NotImplementedError
