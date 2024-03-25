from prorch.utils.constants import Status


class StatusManagerMixin:
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
