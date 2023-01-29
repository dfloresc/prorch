from orchestrator.utils import IRepository


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