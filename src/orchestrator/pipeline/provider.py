from typing import List

from orchestrator.pipeline.data_classes import PipelineData
from orchestrator.utils.constants import Metadata
from orchestrator.utils.providers import BaseProvider


class PipelineProvider(BaseProvider):
    _model: str = Metadata.PIPELINES_MODEL

    def get_active_pipelines(self) -> List[PipelineData]:
        pipelines = self._repository.search(filter=["status", "pending"])

        return (
            [PipelineData(**data) for data in pipelines]
            if pipelines
            else []
        )

    def get_pipeline_by_uuid(self, uuid) -> PipelineData:
        pipeline = self._repository.get(uuid=uuid)

        return PipelineData(**pipeline) if pipeline else None
