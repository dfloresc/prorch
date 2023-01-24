from tinydb import TinyDB, Query
from utils import Repository, SavedItem
from dataclasses import asdict

from .data_classes import PipelineData

class PipelineRepository(Repository):
    def __init__(self):
        self._db = TinyDB("database.json")
        self._table = self._db.table("pipelines")

    def save(self, data: PipelineData) -> SavedItem:
        id = self._table.insert(asdict(data))

        return SavedItem(identifier=id)

    def get(self, uuid: str) -> PipelineData:
        query = Query()
        pipeline_data = self._table.get(query.uuid == uuid)

        return PipelineData(**pipeline_data)

    def update(self, uuid: str, data: PipelineData) -> PipelineData:
        query = Query()
        self._table.update(asdict(data), query.uuid == uuid)
