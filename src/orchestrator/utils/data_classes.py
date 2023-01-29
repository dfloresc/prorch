from dataclasses import dataclass
from typing import Union

from orchestrator.utils.interfaces import IRepository


@dataclass
class SavedItem:
    identifier: Union[str, int]


@dataclass
class OrchestratorConfig:
    repository_class: IRepository