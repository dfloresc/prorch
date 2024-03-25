from typing import Dict, List, Union

from prorch.decorators.decorators import register_pipeline
from prorch.interfaces.repository import IRepository
from prorch.pipeline.pipeline import Pipeline
from prorch.step.step import Step


class TestRepository(IRepository):
    __test__ = False
    """Test repository with all method doing nothing. Those will be mocked"""

    def get(self, uuid: str) -> Dict:
        pass

    def save(self, data: Dict):
        pass

    def update(self, uuid: str, data: Dict) -> Dict:
        pass

    def search(self, filter: List[Union[str, List]]) -> Dict:
        pass


class FirstTestStep(Step):
    name = "FirstTestStep"


@register_pipeline
class TestPipelineWithSteps(Pipeline):
    __test__ = False

    name = "TestPipelineWithSteps"
    steps = [FirstTestStep]


@register_pipeline
class TestPipelineWithoutName(Pipeline):
    __test__ = False

    steps = []


@register_pipeline
class TestPipelineWithoutSteps(Pipeline):
    __test__ = False

    name = "TestPipelineWithoutSteps"
