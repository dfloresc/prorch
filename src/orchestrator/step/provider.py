from typing import List

from orchestrator.step.data_classes import StepData
from orchestrator.utils.constants import Metadata
from orchestrator.utils.providers import BaseProvider


class StepProvider(BaseProvider):
    _model: str = Metadata.STEP_MODEL

    def search_steps_by_pipeline_uuid(
        self,
        pipeline_uuid: str,
    ) -> List[StepData]:
        steps = self._repository.search(["pipeline_uuid", pipeline_uuid])

        return [StepData(**data) for data in steps if steps]
