class ProviderManagerMixin:
    _provider_class = None
    _repository_class = None

    def __init__(self, repository_class):
        self._repository_class = repository_class

        if not self._provider_class:
            raise NotImplementedError

        self._init_provider()

    def _init_provider(self):
        self._provider = self._provider_class(
            repository_class=self._repository_class,
        )

    def _save(self) -> None:
        self._provider.save(data=self.to_dataclass())

    def _update(self):
        self._provider.update(
            uuid=self.uuid,
            data=self.to_dataclass(),
        )
