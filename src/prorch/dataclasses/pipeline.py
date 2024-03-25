from dataclasses import dataclass
from typing import Dict, Union


@dataclass
class PipelineData:
    """dataclass for a pipeline"""

    uuid: str
    name: str
    metadata: Dict[str, Union[str, Dict]]
    status: str
