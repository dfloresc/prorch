# Process Orchestrator

<!-- TOC start -->
- [Summary](#summary)
- [Pipeline and Steps](#pipeline-and-steps)
  * [Step 1: Define the Pipeline](#step-1-define-the-pipeline)
  * [Step 2: Implement the Steps](#step-2-implement-the-steps)
  * [Step 3: Execute the Pipeline](#step-3-execute-the-pipeline)
- [Orchestrator: Managing and Executing Pipelines](#orchestrator-managing-and-executing-pipelines)
  * [Implementing the IRepository Interface](#implementing-the-irepository-interface)
- [Configuring and Using the Orchestrator](#configuring-and-using-the-orchestrator)
<!-- TOC end -->
  
<!-- TOC --><a name="summary"></a>
## Summary

This project aims to develop a process orchestrator. The goal is to break down a large process into smaller, manageable subprocesses, where each one focuses on a specific task and is carried out through a series of steps within a "pipeline".

The core of the proposal is to allow developers to create their own "pipelines", including the corresponding steps, in the code in a simple and efficient way.

In summary, this project seeks to facilitate and optimize the management of large processes by dividing them into smaller, specific subprocesses, thus facilitating their implementation and monitoring.

<!-- TOC --><a name="pipeline-and-steps"></a>
## Pipeline and Steps

To illustrate the application of this orchestrator, consider the example of the backup automation process. This process can be divided into several subprocesses, each of which encompasses a specific task:

1. Backup generation.
2. Transfer of the file to secure storage.
3. Notification of the process completion.

<!-- TOC --><a name="step-1-define-the-pipeline"></a>
### Step 1: Define the Pipeline

Start by defining your pipeline. This involves subclassing `Pipeline` and specifying the sequence of steps it should execute. Use the `@register_pipeline` decorator to register the pipeline class.

```python
from prorch.pipeline.pipeline import Pipeline
from prorch.decorators.decorators import register_pipeline

@register_pipeline
class  BackupAutomationPipeline(Pipeline):
	name = "BackupAutomationPipeline"
	steps = [BackupGeneration, BackupTransfer, ProcessCompletionNotification]
```

<!-- TOC --><a name="step-2-implement-the-steps"></a>
### Step 2: Implement the Steps

Each step in the backup process is implemented as a subclass of Step. Inside each step, you define its behavior through the on_start and on_continue methods, utilizing the OnStartMixin and OnContinueMixin for additional functionalities.

```python

from prorch.step.step import Step
from prorch.mixins.on_start import OnStartMixin
from prorch.mixins.on_continue import OnContinueMixin
from prorch.decorators.decorators import register_step


@register_step
class  BackupGeneration(OnStartMixin,  OnContinueMixin,  Step):
name = "BackupGeneration"

def  on_start(self):
	# Logic for initiating the backup generation
	print("Starting the backup generation process.")

def  on_continue(self):
	# Logic to proceed with backup generation
	print("Backup generation completed.")
	self.finish() # not necessary in first execution
```

Continue implementing the remaining steps  (BackupTransfer,  and ProcessCompletionNotification)  in a similar manner, making sure to define the specific logic for each step's on_start and on_continue methods.

<!-- TOC --><a name="step-3-execute-the-pipeline"></a>
### Step 3: Execute the Pipeline

With the steps defined, you can now execute the pipeline. The pipeline execution can be triggered through your application logic, scheduling mechanisms,  or an event-driven trigger, depending on your project's requirements.

Ensure you have instantiated the BackupAutomationPipeline and call its execution method according to the framework's execution model.

```python
# Example of pipeline execution
pipeline = BackupAutomationPipeline(repository_class=TinyDBRepository)
pipeline.start()
```

Customize each step according to your specifications and operational environment.

<!-- TOC --><a name="orchestrator-managing-and-executing-pipelines"></a>
## Orchestrator: Managing and Executing Pipelines

The `Orchestrator` class is designed to manage and execute pipelines that are marked as pending. It works by interfacing with a repository that stores the pipeline data, making use of the `IRepository` interface to ensure a standard structure for repository implementations.

<!-- TOC --><a name="implementing-the-irepository-interface"></a>
### Implementing the IRepository Interface

To utilize the `Orchestrator`, an implementation of the `IRepository` interface is required. This interface is crucial for storing and managing pipeline information in a structured way. The `IRepository` interface mandates the implementation of several methods to support basic CRUD (Create, Read, Update, Delete) operations on the pipeline data. The methods required to be overridden in any implementing class are:

- `get(uuid: str) -> Dict`: Retrieves an item by its unique identifier (UUID).

- `save(data: Dict) -> Dict`: Saves an item to the repository and returns information about the saved item.

- `update(uuid: str, data: Dict) -> None`: Updates an existing item identified by its UUID.

- `search(filter: List[Union[str, List]]) -> List[Dict]`: Searches for items matching specified criteria.

Following the interface's requirements, below is an example of how to implement the `IRepository` using TinyDB, a lightweight document-oriented database.

```python
from tinydb import TinyDB, where
from typing import Dict, List, Union

from prorch.dataclasses.orchestrator import SavedItem
from prorch.interfaces.repository import IRepository
from prorch.utils.constants import Metadata

class TinyDBRepository(IRepository):
    def __init__(self, model: str):
        super().__init__(model)
        self._db = TinyDB("database.json")
        self._table = self._db.table(Metadata.TABLE_NAMES[model])

    def get(self, uuid: str) -> Dict:
        return self._table.get(where("uuid") == uuid)

    def save(self, data: Dict) -> SavedItem:
        id = self._table.insert(data)

        return SavedItem(identifier=id)

    def update(self, uuid: str, data: Dict) -> None:
        self._table.update(data, where("uuid") == uuid)

    def search(self, filter: List[Union[str, List]]) -> List[Dict]:
        field, value = filter

        return self._table.search(where(field) == value)

```

This implementation outlines how to adhere to the `IRepository` interface using TinyDB, showcasing the necessary methods and their purpose within the context of managing pipeline data.

<!-- TOC --><a name="configuring-and-using-the-orchestrator"></a>
## Configuring and Using the Orchestrator

With a repository implemented, you can configure and instantiate the Orchestrator to manage and execute pipelines. Here's a simple example using TinyDBRepository as the repository class:

```python

from prorch.dataclasses.orchestrator import OrchestratorConfig
from your_repository_implementation import TinyDBRepository # Ensure to replace this with your actual repository class

from prorch.orchestrator import Orchestrator

# Configuration for the orchestrator
orchestrator_config = OrchestratorConfig(repository_class=TinyDBRepository)

# Instantiate the orchestrator
orchestrator = Orchestrator(config=orchestrator_config)

# Execute all pending pipelines
orchestrator.execute_pipelines()
```

This setup demonstrates how to prepare the Orchestrator for running pipelines that are marked as pending within your repository. The Orchestrator fetches all active pipelines and executes them, facilitating automated process management in your application.
