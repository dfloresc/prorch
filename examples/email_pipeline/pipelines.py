from steps import GenerateAudience, GenerateCache, SendEmail

from prorch.decorators.decorators import register_pipeline
from prorch.pipeline.pipeline import Pipeline


@register_pipeline
class EmailPipeline(Pipeline):
    name = "EmailPipeline"
    steps = [GenerateAudience, GenerateCache, SendEmail]
