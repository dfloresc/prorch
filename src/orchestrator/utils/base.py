from orchestrator.utils.constants import Status


class StatusManager:
    def _update_status(self, status: Status):
        self.status = status
        self._update()

    def start(self):
        self._update_status(Status.PENDING)

    def finish(self):
        self._update_status(Status.FINISHED)

    def fail(self):
        self._update_status(Status.FAILED)

    def cancel(self):
        self._update_status(Status.CANCELLED)


class ProviderManager:
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


class BaseOrchestrator(StatusManager, ProviderManager):
    def to_dataclass(self):
        raise NotImplementedError
