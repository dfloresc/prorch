from collections import Counter
from typing import Dict, List, Tuple
from uuid import uuid4

from prorch.dataclasses.pipeline import PipelineData
from prorch.dataclasses.step import StepData
from prorch.exceptions.exceptions import PipelineNameNotDefinedException, StepsNotDefinedException
from prorch.interfaces.repository import IRepository
from prorch.providers.pipeline_provider import PipelineProvider
from prorch.step import services as StepServices
from prorch.utils.base import BaseOrchestrator
from prorch.utils.constants import Status


class Pipeline(BaseOrchestrator):
    uuid: str = None
    name: str = None
    steps: List[str] = None
    metadata: Dict = {"current_step": None}
    status: str = None

    _repository_class: IRepository
    _provider_class = PipelineProvider

    def __init__(
        self,
        repository_class: IRepository,
        pipeline_uuid: str = None,
    ):
        super().__init__(repository_class)

        self._validate_pipeline_name()
        self._validate_pipeline_steps()
        self._init_instance(pipeline_uuid=pipeline_uuid)

    def _init_instance(self, pipeline_uuid: str):
        if not pipeline_uuid:
            self._create_instance()
        else:
            self._load_instance(pipeline_uuid=pipeline_uuid)

    def _validate_pipeline_name(self) -> bool:
        if not self.name:
            raise PipelineNameNotDefinedException

        return True

    def _validate_pipeline_steps(self) -> bool:
        if not self.steps or not len(self.steps):
            raise StepsNotDefinedException

        return True

    def _check_action_needed(self, steps: List[StepData]) -> Tuple[bool, bool, bool]:
        steps_status_mapped = Counter([step.status for step in steps])

        must_fail = steps_status_mapped[Status.FAILED] > 0
        must_cancel = steps_status_mapped[Status.CANCELLED] > 0
        must_finish = steps_status_mapped[Status.FINISHED] == len(steps)

        return must_fail, must_cancel, must_finish

    def _should_continue(self, steps: List[StepData]) -> bool:
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

    def _get_current_step_instance(self, steps: List[StepData], repository_class: IRepository):
        wanted_step = None
        instance = None

        for step in steps:
            if step.status in [Status.CREATED, Status.PENDING]:
                wanted_step = step
                break

        if wanted_step:
            instance = StepServices.get_step_instance(
                step_data=wanted_step, repository_class=repository_class
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
            # instance for creation only
            _ = step(repository_class=self._repository_class, pipeline_uuid=self.uuid)

    def _load_instance(self, pipeline_uuid: str):
        pipeline_data = self._get(uuid=pipeline_uuid)

        self.uuid = pipeline_data.uuid
        self.status = pipeline_data.status
        self.metadata = pipeline_data.metadata

    def _get(self, uuid: str) -> PipelineData:
        return self._provider.get_pipeline_by_uuid(uuid=uuid)

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
