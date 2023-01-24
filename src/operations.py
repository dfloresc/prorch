from pipeline import Pipeline
from step import Step
from utils import register_step

# steps
@register_step
class GenerateAudience(Step):
    name = "GenerateAudience"

@register_step
class GenerateCache(Step):
    name = "GenerateCache"
    pass

@register_step
class SendEmail(Step):
    name = "SendEmail"
    pass

# pipeline
class EmailPipeline(Pipeline):
    name = "email_pipeline"
    steps = [GenerateAudience, GenerateCache, SendEmail]
