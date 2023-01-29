from dataclasses import asdict
from typing import List, Dict

from orchestrator.utils import BaseProvider, Metadata
from orchestrator.step import StepData


class StepProvider(BaseProvider):
    _model: str = Metadata.STEP_MODEL

    def search_steps_by_pipeline_uuid(
        self,
        pipeline_uuid: str,
    ) -> List[StepData]:
        steps = self._repository.search(["pipeline_uuid", pipeline_uuid])

        return [StepData(**data) for data in steps if steps]

    def save_step(self, data: Dict):
        self._repository.save(data=asdict(data))

    def update_step(self, uuid: str, data: Dict):
        self._repository.update(uuid=uuid, data=asdict(data))
