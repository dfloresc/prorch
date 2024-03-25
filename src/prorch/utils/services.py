from .constants import PIPELINES, STEPS


def get_step_class(class_name):
    return STEPS.get(class_name)


def get_pipeline_class(class_name):
    return PIPELINES.get(class_name)
