import pytest

from conftest import (
    TestPipelineWithoutName,
    TestPipelineWithoutSteps,
    TestPipelineWithSteps,
    TestRepository,
)
from orchestrator.utils.exceptions import (
    PipelineNameNotDefinedException,
    StepsNotDefinedException,
)
from orchestrator.step.data_classes import StepData
from orchestrator.utils.constants import Status


class TestPipeline:
    def test_pipeline_without_name_should_raise_exception(self):
        with pytest.raises(PipelineNameNotDefinedException):
            TestPipelineWithoutName(repository_class=TestRepository)

    def test_pipeline_without_steps_should_raise_exception(self):
        with pytest.raises(StepsNotDefinedException):
            TestPipelineWithoutSteps(repository_class=TestRepository)

    def test_pipeline_should_not_raise_exception(self, mocker):
        instance = TestPipelineWithSteps(repository_class=TestRepository)

        assert isinstance(instance, TestPipelineWithSteps)

    def test_pipeline_should_create_a_new_instance(self, mocker):
        mocked_create_instance = mocker.patch(
            "conftest.TestPipelineWithSteps._create_instance",
            return_value={}
        )

        TestPipelineWithSteps(repository_class=TestRepository)

        mocked_create_instance.assert_called_once()

    def test_pipeline_should_load_a_created_instance(self, mocker):
        mocked_load_instance = mocker.patch(
            "conftest.TestPipelineWithSteps._load_instance",
            return_value={}
        )

        TestPipelineWithSteps(
            repository_class=TestRepository,
            pipeline_uuid="mocked",
        )

        mocked_load_instance.assert_called_once()

    @pytest.mark.parametrize(["steps", "expected_results"], [
        [
            [
                StepData(
                    uuid="mocked",
                    name="mocked",
                    pipeline_uuid="mocked",
                    metadata={},
                    status=Status.FAILED
                ),
                StepData(
                    uuid="mocked",
                    name="mocked",
                    pipeline_uuid="mocked",
                    metadata={},
                    status=Status.CREATED
                ),
            ],
            (True, False, False),
        ],
        [
            [
                StepData(
                    uuid="mocked",
                    name="mocked",
                    pipeline_uuid="mocked",
                    metadata={},
                    status=Status.CREATED
                ),
                StepData(
                    uuid="mocked",
                    name="mocked",
                    pipeline_uuid="mocked",
                    metadata={},
                    status=Status.CREATED
                ),
            ],
            (False, False, False),
        ],
        [
            [
                StepData(
                    uuid="mocked",
                    name="mocked",
                    pipeline_uuid="mocked",
                    metadata={},
                    status=Status.FINISHED
                ),
                StepData(
                    uuid="mocked",
                    name="mocked",
                    pipeline_uuid="mocked",
                    metadata={},
                    status=Status.CANCELLED
                ),
            ],
            (False, True, False),
        ],
        [
            [
                StepData(
                    uuid="mocked",
                    name="mocked",
                    pipeline_uuid="mocked",
                    metadata={},
                    status=Status.FINISHED
                ),
                StepData(
                    uuid="mocked",
                    name="mocked",
                    pipeline_uuid="mocked",
                    metadata={},
                    status=Status.FINISHED
                ),
            ],
            (False, False, True),
        ],
    ])
    def test_pipeline_check_action_needed(
        self,
        mocker,
        steps,
        expected_results
    ):
        mocked_create_instance = mocker.patch(
            "conftest.TestPipelineWithSteps._create_instance",
            return_value={}
        )

        instance = TestPipelineWithSteps(repository_class=TestRepository)
        result = instance._check_action_needed(steps=steps)

        mocked_create_instance.assert_called_once()
        assert result == expected_results
