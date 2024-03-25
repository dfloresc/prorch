from prorch.decorators.decorators import register_step
from prorch.mixins.on_continue import OnContinueMixin
from prorch.mixins.on_start import OnStartMixin
from prorch.step.step import Step


@register_step
class GenerateAudience(OnStartMixin, OnContinueMixin, Step):
    name = "GenerateAudience"

    def on_start(self):
        print("GenerateAudience AfterStarting")

    def on_continue(self):
        print("GenerateAudience AfterContinue")
        self.finish()


@register_step
class GenerateCache(OnStartMixin, OnContinueMixin, Step):
    name = "GenerateCache"

    def on_start(self):
        print("GenerateCache AfterStarting")

    def on_continue(self):
        print("GenerateCache AfterContinue")
        self.fail()


@register_step
class SendEmail(OnStartMixin, OnContinueMixin, Step):
    name = "SendEmail"

    def on_start(self):
        print("SendEmail AfterStarting")

    def on_continue(self):
        print("SendEmail AfterContinue")
        self.finish()
