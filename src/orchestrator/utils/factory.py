from typing import List

from orchestrator.pipeline.data_classes import PipelineData
from orchestrator.pipeline import services as pipeline_services
from orchestrator.utils import services as UtilServices
from orchestrator.utils.data_classes import OrchestratorConfig
from orchestrator.utils.interfaces import IRepository


class Orchestrator:
    _repository_class: IRepository = None

    def __init__(self, config: OrchestratorConfig):
        self._repository_class = config.repository_class

    def get_active_pipelines(self) -> List[PipelineData]:
        return pipeline_services.get_active_pipelines(
            repository_class=self._repository_class,
        )

    def execute_pipelines(self) -> None:
        active_pipelines = self.get_active_pipelines()

        if active_pipelines:
            for pipeline in active_pipelines:
                pipeline_class = UtilServices.get_pipeline_class(pipeline.name)
                instance = pipeline_class(
                    pipeline_uuid=pipeline.uuid,
                    repository_class=self._repository_class,
                )
                instance.start()
