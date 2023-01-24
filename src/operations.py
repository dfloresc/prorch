from pipeline import Pipeline
from step import Step

# steps
class GenerateAudience(Step):
    name = "GenerateAudience"

class GenerateCache(Step):
    name = "GenerateCache"
    pass

class SendEmail(Step):
    name = "SendEmail"
    pass

# pipeline
class EmailPipeline(Pipeline):
    name = "email_pipeline"
    steps = [GenerateAudience, GenerateCache, SendEmail]
