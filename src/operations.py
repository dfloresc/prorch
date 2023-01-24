import step
import pipeline
from utils import register_step


# steps
@register_step
class GenerateAudience(step.OnStart, step.OnContinue, step.Step):
    name = "GenerateAudience"

    def on_start(self):
        print("AfterStarting")

    def on_continue(self):
        print("AfterContinue")
        self.finish()


@register_step
class GenerateCache(step.OnStart, step.OnContinue, step.Step):
    name = "GenerateCache"

    def on_start(self):
        print("AfterStarting")

    def on_continue(self):
        print("AfterContinue")
        self.finish()


@register_step
class SendEmail(step.OnStart, step.OnContinue, step.Step):
    name = "SendEmail"

    def on_start(self):
        print("AfterStarting")

    def on_continue(self):
        print("AfterContinue")
        self.finish()


# pipeline
class EmailPipeline(pipeline.Pipeline):
    name = "email_pipeline"
    steps = [GenerateAudience, GenerateCache, SendEmail]
