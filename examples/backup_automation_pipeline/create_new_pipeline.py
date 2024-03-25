from pipelines import BackupAutomationPipeline
from repository import TinyDBRepository

email_pipeline = BackupAutomationPipeline(repository_class=TinyDBRepository)
email_pipeline.start()
