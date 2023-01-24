from typing import List

from .repository import PipelineRepository
from .data_classes import PipelineData

from orchestrator.utils import UtilServices

def get_active_pipelines() -> List[PipelineData]:
    repository = PipelineRepository()

    return repository.get_active_pipelines()


def execute_all_active_pipelines() -> None:
    active_pipelines = get_active_pipelines()

    if active_pipelines:
        for pipeline in active_pipelines:
            pipeline_class = UtilServices.get_pipeline_class(pipeline.name)
            instance = pipeline_class(pipeline.uuid)
            instance.start()