from prorch.mixins.provider_manager import ProviderManagerMixin
from prorch.mixins.status_manager import StatusManagerMixin


class BaseOrchestrator(StatusManagerMixin, ProviderManagerMixin):
    def to_dataclass(self):
        raise NotImplementedError
