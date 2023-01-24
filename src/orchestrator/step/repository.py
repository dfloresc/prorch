from typing import List
from tinydb import TinyDB, Query
from orchestrator.utils import Repository, SavedItem
from dataclasses import asdict

from .data_classes import StepData

class StepRepository(Repository):
    def __init__(self):
        self._db = TinyDB("database.json")
        self._table = self._db.table("pipeline_steps")

    def save(self, data: StepData) -> SavedItem:
        id = self._table.insert(asdict(data))

        return SavedItem(identifier=id)

    def get(self, uuid: str) -> StepData:
        pass

    def update(self, uuid: str, data: StepData) -> StepData:
        query = Query()
        self._table.update(asdict(data), query.uuid == uuid)

    def search_by_pipeline_uuid(self, pipeline_uuid: str) -> List[StepData]:
        query = Query()
        steps_data = self._table.search(query.pipeline_uuid == pipeline_uuid)

        return [StepData(**step) for step in steps_data]