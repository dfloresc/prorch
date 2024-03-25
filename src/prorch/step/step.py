from typing import Dict
from uuid import uuid4

from prorch.dataclasses.step import StepData
from prorch.exceptions.exceptions import PipelineNotDefinedException, StepNameNotDefinedException
from prorch.interfaces.repository import IRepository
from prorch.providers.step_provider import StepProvider
from prorch.utils.base import BaseOrchestrator
from prorch.utils.constants import Status


class Step(BaseOrchestrator):
    uuid: str = None
    name: str = None
    pipeline_uuid: str = None
    metadata: Dict = {}
    status: str

    _repository_class: IRepository
    _provider_class = StepProvider

    def __init__(self, repository_class, pipeline_uuid: str = None, step_data: StepData = None):
        super().__init__(repository_class)
        self._validate_name()

        if step_data:
            self._load_instance(step_data=step_data)
        else:
            self._validate_pipeline_uuid(pipeline_uuid=pipeline_uuid)
            self._create_instance(pipeline_uuid=pipeline_uuid)

    def _load_instance(self, step_data: StepData):
        self.uuid = step_data.uuid
        self.pipeline_uuid = step_data.pipeline_uuid
        self.metadata = step_data.metadata
        self.status = step_data.status

    def _create_instance(self, pipeline_uuid: str):
        self.uuid = str(uuid4())
        self.pipeline_uuid = pipeline_uuid
        self.status = Status.CREATED
        self._save()

    def _validate_pipeline_uuid(self, pipeline_uuid: str) -> bool:
        if not pipeline_uuid:
            raise PipelineNotDefinedException

        return True

    def _validate_name(self) -> bool:
        if not self.name:
            raise StepNameNotDefinedException

        return True

    def to_dataclass(self) -> StepData:
        return StepData(
            uuid=self.uuid,
            name=self.name,
            pipeline_uuid=self.pipeline_uuid,
            metadata=self.metadata,
            status=self.status,
        )

    def _continue(self) -> None:
        if self.status in [Status.CANCELLED, Status.FAILED, Status.FINISHED]:
            return

        # do something through the onContinue mixin
