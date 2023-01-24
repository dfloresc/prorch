from orchestrator import step
from orchestrator.step.mixins import OnStart, OnContinue
from orchestrator.utils import register_step


@register_step
class GenerateAudience(OnStart, OnContinue, step.Step):
    name = "GenerateAudience"

    def on_start(self):
        print("GenerateAudience AfterStarting")

    def on_continue(self):
        print("GenerateAudience AfterContinue")
        self.finish()


@register_step
class GenerateCache(OnStart, OnContinue, step.Step):
    name = "GenerateCache"

    def on_start(self):
        print("GenerateCache AfterStarting")

    def on_continue(self):
        print("GenerateCache AfterContinue")
        self.fail()


@register_step
class SendEmail(OnStart, OnContinue, step.Step):
    name = "SendEmail"

    def on_start(self):
        print("SendEmail AfterStarting")

    def on_continue(self):
        print("SendEmail AfterContinue")
        self.finish()