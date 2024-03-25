from dataclasses import dataclass
from typing import Union

from prorch.interfaces.repository import IRepository


@dataclass
class SavedItem:
    identifier: Union[str, int]


@dataclass
class OrchestratorConfig:
    repository_class: IRepository
