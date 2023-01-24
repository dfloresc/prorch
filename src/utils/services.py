from .constants import STEPS

def get_step_class_instance(class_name):
    return STEPS.get(class_name)