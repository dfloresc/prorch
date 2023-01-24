from typing import List, Dict
from uuid import uuid4

from orchestrator.utils.exceptions import (
    StepsNotDefinedException,
    PipelineNameNotDefinedException,
)
from orchestrator.utils.constants import Status
from .data_classes import PipelineData
from .repository import PipelineRepository
from orchestrator.step import StepServices

class Pipeline:
    uuid: str = None
    name: str = None
    steps: List[str] = None
    metadata: Dict = {"current_step": None}
    status: str = None

    def __init__(self, pipeline_uuid: str = None):
        self._validate_pipeline_name()
        self._validate_pipeline_steps()

        self._init_repository()
        self._init_instance(pipeline_uuid=pipeline_uuid)

    def _init_instance(self, pipeline_uuid: str):
        if not pipeline_uuid:
            self._create_instance()
        else:
            self._load_instance(pipeline_uuid=pipeline_uuid)

    def _init_repository(self):
        self._repository = PipelineRepository() # could be an inversed dependency but i wan't complex it.

    def _validate_pipeline_name(self) -> bool:
        if not self.name:
            raise PipelineNameNotDefinedException

        return True

    def _validate_pipeline_steps(self) -> bool:
        if not len(self.steps):
            raise StepsNotDefinedException

        return True

    def _get_current_step_instance(self): # TODO: put dataclass as typing
        steps = StepServices.search_by_pipeline_uuid(pipeline_uuid=self.uuid)
        wanted_step = None
        instance = None

        if all([step.status == Status.FINISHED for step in steps]):
            self.finish()
            return

        for step in steps:
            if step.status == Status.FAILED:
                self.fail()
                break

            if step.status == Status.CANCELLED:
                self.cancel()
                break

            if step.status in [Status.CREATED, Status.PENDING]:
                wanted_step = step
                break

        if wanted_step:
            instance = StepServices.get_step_instance(step_data=wanted_step)

        return instance

    def to_dataclass(self) -> PipelineData:
        return PipelineData(
            uuid=self.uuid,
            name=self.name,
            metadata=self.metadata,
            status=self.status,
        )

    def _create_instance(self):
        self.uuid = str(uuid4())
        self.status = Status.CREATED
        self._repository.save(
            data=self.to_dataclass(),
        )

        for step in self.steps:
            # only for creating register in repository
            _ = step(pipeline_uuid=self.uuid)

    def _update(self):
        self._repository.update(
            uuid=self.uuid,
            data=self.to_dataclass(),
        )

    def _load_instance(self, pipeline_uuid: str):
        pipeline_data = self._get(pipeline_uuid)

        self.uuid = pipeline_data.uuid
        self.status = pipeline_data.status
        self.metadata = pipeline_data.metadata

    def _get(self, pipeline_uuid: str) -> PipelineData:
        return self._repository.get(pipeline_uuid)

    def fail(self):
        self.status = Status.FAILED
        self._update()

    def cancel(self):
        self.status = Status.CANCELLED
        self._update()

    def finish(self):
        self.status = Status.FINISHED
        self._update()

    def start(self):
        current_step = self._get_current_step_instance()

        if current_step:
            if current_step.status == Status.CREATED:
                current_step.start()

            if current_step.status == Status.PENDING:
                current_step._continue()

            self.metadata["current_step"] = current_step.uuid
            self.status = Status.PENDING
            self._update()
