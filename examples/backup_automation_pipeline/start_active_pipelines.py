from pipelines import *
from repository import TinyDBRepository

from prorch.orchestrator.orchestrator import Orchestrator, OrchestratorConfig

orchestrator_config = OrchestratorConfig(repository_class=TinyDBRepository)
orchestrator = Orchestrator(config=orchestrator_config)
orchestrator.execute_pipelines()
