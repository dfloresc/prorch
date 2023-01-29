from dataclasses import dataclass
from typing import Dict, Union


@dataclass
class StepData:
    uuid: str
    name: str
    pipeline_uuid: str
    metadata: Dict[str, Union[str, Dict]]
    status: str
