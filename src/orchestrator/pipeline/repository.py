from typing import List
from tinydb import TinyDB, Query
from orchestrator.utils import Repository, SavedItem, Status
from dataclasses import asdict, make_dataclass

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

    def get_active_pipelines(self) -> List[PipelineData]:
        query = Query()
        active_pipelines = self._table.search(query.status == Status.PENDING)
        pipelines_data = [PipelineData(**data) for data in active_pipelines if active_pipelines]

        return pipelines_data