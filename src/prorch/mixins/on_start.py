class OnStartMixin:
    def start(self):
        super().start()
        self.on_start()

    def on_start(self):
        raise NotImplementedError
