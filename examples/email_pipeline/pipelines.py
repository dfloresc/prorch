from orchestrator import pipeline
from orchestrator.utils import register_pipeline

from steps import GenerateAudience, GenerateCache, SendEmail


@register_pipeline
class EmailPipeline(pipeline.Pipeline):
    name = "EmailPipeline"
    steps = [GenerateAudience, GenerateCache, SendEmail]
