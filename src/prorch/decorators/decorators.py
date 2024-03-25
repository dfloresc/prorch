from prorch.utils.constants import PIPELINES, STEPS


def register_pipeline(pipeline_class):
    PIPELINES.update({pipeline_class.name: pipeline_class})

    return pipeline_class


def register_step(step_class):
    STEPS.update({step_class.name: step_class})

    return step_class
