PIPELINES = {}
STEPS = {}


class Metadata:
    PIPELINES_MODEL = "PIPELINE"
    STEP_MODEL = "STEP"

    TABLE_NAMES = {
        PIPELINES_MODEL: "pipelines",
        STEP_MODEL: "pipeline_steps",
    }


class Status:
    CREATED = "created"
    PENDING = "pending"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    FAILED = "failed"
