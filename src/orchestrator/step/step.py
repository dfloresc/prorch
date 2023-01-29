from typing import Dict
from uuid import uuid4

from orchestrator.step.provider import StepProvider

from .data_classes import StepData
from orchestrator.utils.exceptions import (
    StepNameNotDefinedException,
    PipelineNotDefinedException
)
from orchestrator.utils.constants import Status
from orchestrator.utils import IRepository


class Step:
    uuid: str = None
    name: str = None
    pipeline_uuid: str = None
    metadata: Dict = {}
    status: str
    _repository_class: IRepository

    def __init__(
        self,
        repository_class,
        pipeline_uuid: str = None,
        step_data: StepData = None
    ):
        self._validate_name()

        self._repository_class = repository_class
        self._init_repository()

        if step_data:
            self._load_instance(step_data=step_data)
        else:
            self._validate_pipeline_uuid(pipeline_uuid=pipeline_uuid)
            self._create_instance(pipeline_uuid=pipeline_uuid)

    def _init_repository(self):
        self._provider = StepProvider(
            repository_class=self._repository_class,
        )

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
            status=self.status
        )

    def _save(self) -> None:
        self._provider.save_step(data=self.to_dataclass())

    def _update(self):
        self._provider.update_step(uuid=self.uuid, data=self.to_dataclass())

    def start(self) -> None:
        self.status = Status.PENDING
        self._update()

    def _continue(self) -> None:
        if self.status in [Status.CANCELLED, Status.FAILED, Status.FINISHED]:
            return

        # use mixin to implement `on_continue` logic

    def stop(self) -> None:
        self.status = Status.CANCELLED
        self._update()

    def fail(self) -> None:
        self.status = Status.FAILED
        self._update()

    def finish(self) -> None:
        self.status = Status.FINISHED
        self._update()
