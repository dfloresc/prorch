from prorch.decorators.decorators import register_pipeline, register_step
from prorch.mixins.on_continue import OnContinueMixin
from prorch.mixins.on_start import OnStartMixin
from prorch.pipeline.pipeline import Pipeline
from prorch.step.step import Step

@register_step
class BackupGeneration(OnStartMixin, OnContinueMixin, Step):
    name = "BackupGeneration"

    def on_start(self):
        print("Starting the backup generation process.")

    def on_continue(self):
        print("Backup generation completed.")
        self.finish()

@register_step
class BackupTransfer(OnStartMixin, OnContinueMixin, Step):
    name = "BackupTransfer"

    def on_start(self):
        print("Starting the process of transferring the backup to secure storage.")

    def on_continue(self):
        print("Backup transfer completed.")
        self.finish()

@register_step
class ProcessCompletionNotification(OnStartMixin, OnContinueMixin, Step):
    name = "ProcessCompletionNotification"

    def on_start(self):
        print("Initiating process completion notification.")

    def on_continue(self):
        print("Notification sent. Backup process completed.")
        self.finish()



@register_pipeline
class BackupAutomationPipeline(Pipeline):
    name = "BackupAutomationPipeline"
    steps = [BackupGeneration, BackupTransfer, ProcessCompletionNotification]
