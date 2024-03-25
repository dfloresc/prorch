class OnContinueMixin:
    def _continue(self):
        super()._continue()
        self.on_continue()

    def on_continue(self):
        raise NotImplementedError
