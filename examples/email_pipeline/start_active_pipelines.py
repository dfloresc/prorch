from prorch.orchestrator.orchestrator import Orchestrator, OrchestratorConfig
from pipelines import *
from tinydb_repository import TinyDBRepository


orchestrator_config = OrchestratorConfig(repository_class=TinyDBRepository)
orchestrator = Orchestrator(config=orchestrator_config)
orchestrator.execute_pipelines()
