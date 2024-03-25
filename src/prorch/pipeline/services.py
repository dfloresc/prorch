from typing import List

from prorch.dataclasses.pipeline import PipelineData
from prorch.providers.pipeline_provider import PipelineProvider
from prorch.interfaces.repository import IRepository


def get_active_pipelines(repository_class: IRepository) -> List[PipelineData]:
    provider = PipelineProvider(repository_class=repository_class)

    return provider.get_active_pipelines()
