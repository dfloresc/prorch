from orchestrator.pipeline.pipeline import Pipeline
from orchestrator.utils.decorators import register_pipeline

from steps import GenerateAudience, GenerateCache, SendEmail


@register_pipeline
class EmailPipeline(Pipeline):
    name = "EmailPipeline"
    steps = [GenerateAudience, GenerateCache, SendEmail]
