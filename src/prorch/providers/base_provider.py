from dataclasses import asdict
from typing import Dict

from prorch.interfaces.repository import IRepository


class BaseProvider:
    _model: str
    _repository: IRepository

    def __init__(self, repository_class: IRepository):
        if not self._model:
            raise NotImplementedError

        self.repository_class = repository_class
        self._init_repository()

    def _init_repository(self):
        self._repository = self.repository_class(self._model)

    def save(self, data: Dict):
        self._repository.save(data=asdict(data))

    def update(self, uuid: str, data: Dict):
        self._repository.update(uuid=uuid, data=asdict(data))
