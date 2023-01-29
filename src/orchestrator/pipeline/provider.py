from typing import List, Dict
from orchestrator.utils import Metadata, BaseProvider
from dataclasses import asdict

from .data_classes import PipelineData


class PipelineProvider(BaseProvider):
    _model: str = Metadata.PIPELINES_MODEL

    def get_active_pipelines(self) -> List[PipelineData]:
        pipelines = self._repository.search(["status", "pending"])

        return [PipelineData(**data) for data in pipelines if pipelines]

    def get_pipeline_by_uuid(self, uuid) -> PipelineData:
        pipeline = self._repository.get(uuid=uuid)

        return PipelineData(**pipeline)

    def save_pipeline(self, data: Dict):
        self._repository.save(data=asdict(data))

    def update_pipeline(self, uuid: str, data: Dict):
        self._repository.update(uuid=uuid, data=asdict(data))
