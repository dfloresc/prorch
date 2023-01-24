from src import Pipeline, Step

# steps
class GenerateAudience(Step):
    name = "GenerateAudience"

class GenerateCache(Step):
    pass

class SendEmail(Step):
    pass

# pipeline
class EmailPipeline(Pipeline):
    name = "email_pipeline"
    steps = [GenerateAudience, GenerateCache, SendEmail]
