from typing import List

from orchestrator.pipeline.data_classes import PipelineData
from orchestrator.pipeline.provider import PipelineProvider
from orchestrator.utils.interfaces import IRepository


def get_active_pipelines(repository_class: IRepository) -> List[PipelineData]:
    provider = PipelineProvider(repository_class=repository_class)

    return provider.get_active_pipelines()
