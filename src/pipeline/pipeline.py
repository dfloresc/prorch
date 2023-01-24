from typing import List, Dict
from uuid import uuid4

from exceptions import (
    StepsNotDefinedException,
    PipelineNameNotDefinedException,
)
from .data_classes import PipelineData
from .repository import PipelineRepository
from step import Step

class Pipeline:
    uuid: str = None
    name: str = None
    steps: List[str] = None
    metadata: Dict = {"current_step": None}
    status: str = None

    def __init__(self, pipeline_uuid: str = None):
        self._validate_pipeline_name()
        self._validate_pipeline_steps()

        self._repository = PipelineRepository() # could be an inversed dependency but i wan't complex it.

        if not pipeline_uuid:
            self.uuid = str(uuid4())
            self.status = "PENDING"
            self._create()

        # TODO: get context when pipeline_uuid is passed

    def _validate_pipeline_name(self) -> bool:
        if not self.name:
            raise PipelineNameNotDefinedException

        return True

    def _validate_pipeline_steps(self) -> bool:
        if not len(self.steps):
            raise StepsNotDefinedException

        return True

    def _get_current_step_instance(self) -> Step:
        current_step = None

        if not self.metadata.get("current_step") and len(self.steps):
            step_class = self.steps[0]
            current_step = step_class(pipeline_uuid=self.uuid)

        # TODO: get current step when it exists

        return current_step

    def to_dataclass(self) -> PipelineData:
        return PipelineData(
            uuid=self.uuid,
            name=self.name,
            metadata=self.metadata,
            status=self.status,
        )

    def _create(self):
        self._repository.save(
            data=self.to_dataclass(),
        )

        for step in self.steps:
            step_instance = step(pipeline_uuid=self.uuid)

    def _update(self):
        self._repository.update(
            uuid=self.uuid,
            data=self.to_dataclass(),
        )

    def start(self):
        current_step = self._get_current_step_instance()

        if current_step:
            current_step.start()
            self.metadata["current_step"] = current_step.uuid
            self.status = "IN PROGRESS"
            self._update()
