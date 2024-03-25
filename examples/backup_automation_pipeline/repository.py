from tinydb import TinyDB, where
from typing import Dict, List, Union

from prorch.dataclasses.orchestrator import SavedItem
from prorch.interfaces.repository import IRepository
from prorch.utils.constants import Metadata


class TinyDBRepository(IRepository):
    def __init__(self, model):
        super().__init__(model)

        self._db = TinyDB("database.json")
        self._table = self._db.table(Metadata.TABLE_NAMES[model])

    def get(self, uuid: str) -> Dict:
        return self._table.get(where("uuid") == uuid)

    def save(self, data: Dict) -> SavedItem:
        id = self._table.insert(data)

        return SavedItem(identifier=id)

    def update(self, uuid: str, data: Dict) -> Dict:
        self._table.update(data, where("uuid") == uuid)

    def search(self, filter: List[Union[str, List]]) -> Dict:
        field, value = filter

        return self._table.search(where(field) == value)
