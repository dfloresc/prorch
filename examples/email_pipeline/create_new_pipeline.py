from pipelines import EmailPipeline
from repository import TinyDBRepository

email_pipeline = EmailPipeline(repository_class=TinyDBRepository)
email_pipeline.start()
