import logging

from typing import Dict
from uuid import uuid4

from .repository import StepRepository
from .data_classes import StepData
from exceptions import (
    StepNameNotDefinedException,
    PipelineNotDefinedException,
    RepositoryNotDefinedException,
)

logger = logging.getLogger(__name__)


class Step:
    uuid: str = None
    name: str = None
    pipeline_uuid: str = None
    metadata: Dict = {}
    status: str

    def __init__(self, pipeline_uuid: str):
        # validate data integrity
        self._validate_name()

        self.uuid = str(uuid4())
        self.pipeline_uuid = pipeline_uuid
        self.status = "PENDING"
        self._repository = StepRepository()
        self._save()

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
        self._repository.save(
            data=self.to_dataclass(),
        )

    def _update(self):
        self._repository.update(
            uuid=self.uuid,
            data=self.to_dataclass(),
        )

    def start(self) -> None:
        print("starting step")
        self.status = "IN PROGRESS"
        self._update()
