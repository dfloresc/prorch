from typing import List

from .repository import StepRepository
from .data_classes import StepData
from .step import Step
from orchestrator.utils import UtilServices

def search_by_pipeline_uuid(pipeline_uuid: str) -> List[StepData]:
    repository = StepRepository()

    return repository.search_by_pipeline_uuid(pipeline_uuid=pipeline_uuid)

def get_step_instance(step_data: StepData) -> Step:
    step_class = UtilServices.get_step_class(class_name=step_data.name)
    return step_class(step_data=step_data)