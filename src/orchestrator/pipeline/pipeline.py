from collections import Counter
from typing import List, Dict
from uuid import uuid4

from orchestrator.utils.exceptions import (
    StepsNotDefinedException,
    PipelineNameNotDefinedException,
)
from orchestrator.utils.constants import Status
from orchestrator.utils import IRepository
from .data_classes import PipelineData
from .provider import PipelineProvider
from orchestrator.step import StepServices


class Pipeline:
    uuid: str = None
    name: str = None
    steps: List[str] = None
    metadata: Dict = {"current_step": None}
    status: str = None
    _repository_class: IRepository

    def __init__(
        self,
        repository_class: IRepository,
        pipeline_uuid: str = None,
    ):
        self._validate_pipeline_name()
        self._validate_pipeline_steps()

        self._repository_class = repository_class

        self._init_provider()
        self._init_instance(pipeline_uuid=pipeline_uuid)

    def _init_instance(self, pipeline_uuid: str):
        if not pipeline_uuid:
            self._create_instance()
        else:
            self._load_instance(pipeline_uuid=pipeline_uuid)

    def _init_provider(self):  # todo: abstract
        self._provider = PipelineProvider(
            repository_class=self._repository_class
        )

    def _validate_pipeline_name(self) -> bool:
        if not self.name:
            raise PipelineNameNotDefinedException

        return True

    def _validate_pipeline_steps(self) -> bool:
        if not len(self.steps):
            raise StepsNotDefinedException

        return True

    def _check_action_needed(self, steps):
        steps_status_mapped = Counter([step.status for step in steps])

        must_fail = steps_status_mapped[Status.FAILED] > 0
        must_cancel = steps_status_mapped[Status.CANCELLED] > 0
        must_finish = steps_status_mapped[Status.FINISHED] == len(steps)

        return must_fail, must_cancel, must_finish

    def _should_continue(self, steps):
        should_continue = True
        must_fail, must_cancel, must_finish = self._check_action_needed(steps)

        if must_fail:
            should_continue = False
            self.fail()
        elif must_cancel:
            should_continue = False
            self.cancel()
        elif must_finish:
            should_continue = False
            self.finish()

        return should_continue

    # TODO: put dataclass as typing
    def _get_current_step_instance(self, steps, repository_class):
        wanted_step = None
        instance = None

        for step in steps:
            if step.status in [Status.CREATED, Status.PENDING]:
                wanted_step = step
                break

        if wanted_step:
            instance = StepServices.get_step_instance(
                step_data=wanted_step,
                repository_class=repository_class
            )

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
        self._save()

        for step in self.steps:
            # only for instance rows in repository
            _ = step(
                repository_class=self._repository_class,
                pipeline_uuid=self.uuid
            )

    def _load_instance(self, pipeline_uuid: str):
        pipeline_data = self._get(uuid=pipeline_uuid)

        self.uuid = pipeline_data.uuid
        self.status = pipeline_data.status
        self.metadata = pipeline_data.metadata

    def _get(self, uuid: str) -> PipelineData:
        return self._provider.get_pipeline_by_uuid(uuid=uuid)

    def _save(self):
        self._provider.save_pipeline(data=self.to_dataclass())

    def _update(self):
        self._provider.update_pipeline(
            uuid=self.uuid,
            data=self.to_dataclass()
        )

    def _update_status(self, status: Status):
        self.status = status
        self._update()

    def fail(self):
        self._update_status(Status.FAILED)

    def cancel(self):
        self._update_status(Status.CANCELLED)

    def finish(self):
        self._update_status(Status.FINISHED)

    def start(self):
        steps = StepServices.search_steps_by_pipeline_uuid(
            repository_class=self._repository_class,
            pipeline_uuid=self.uuid,
        )

        if not self._should_continue(steps):
            return

        current_step = self._get_current_step_instance(
            steps=steps,
            repository_class=self._repository_class,
        )

        if current_step:
            if current_step.status == Status.CREATED:
                self.metadata["current_step"] = current_step.uuid
                self.status = Status.PENDING
                current_step.start()
                self._update()

            if current_step.status == Status.PENDING:
                current_step._continue()
