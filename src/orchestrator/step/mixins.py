class OnStart:
    def start(self):
        super().start()
        self.on_start()

    def on_start(self):
        raise NotImplementedError


class OnContinue:
    def _continue(self):
        super()._continue()
        self.on_continue()

    def on_continue(self):
        raise NotImplementedError
