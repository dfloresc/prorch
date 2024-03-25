from typing import List

from prorch.dataclasses.pipeline import PipelineData
from prorch.providers.base_provider import BaseProvider
from prorch.utils.constants import Metadata


class PipelineProvider(BaseProvider):
    _model: str = Metadata.PIPELINES_MODEL

    def get_active_pipelines(self) -> List[PipelineData]:
        pipelines = self._repository.search(filter=["status", "pending"])

        return [PipelineData(**data) for data in pipelines] if pipelines else []

    def get_pipeline_by_uuid(self, uuid) -> PipelineData:
        pipeline = self._repository.get(uuid=uuid)

        return PipelineData(**pipeline) if pipeline else None
