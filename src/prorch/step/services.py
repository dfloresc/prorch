from typing import List

from prorch.dataclasses.step import StepData
from prorch.interfaces.repository import IRepository
from prorch.providers.step_provider import StepProvider
from prorch.step.step import Step
from prorch.utils import services as UtilServices


def search_steps_by_pipeline_uuid(
    repository_class: IRepository,
    pipeline_uuid: str,
) -> List[StepData]:
    provider = StepProvider(repository_class=repository_class)

    return provider.search_steps_by_pipeline_uuid(pipeline_uuid=pipeline_uuid)


def get_step_instance(step_data: StepData, repository_class) -> Step:
    step_class = UtilServices.get_step_class(class_name=step_data.name)
    return step_class(step_data=step_data, repository_class=repository_class)
