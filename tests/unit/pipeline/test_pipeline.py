import pytest

from conftest import (
    TestPipelineWithoutName,
    TestPipelineWithoutSteps,
    TestPipelineWithSteps,
    TestRepository,
)
from prorch.exceptions.exceptions import (
    PipelineNameNotDefinedException,
    StepsNotDefinedException,
)
from prorch.dataclasses.step import StepData
from prorch.utils.constants import Status


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

    @pytest.mark.parametrize(
        [
            "check_action_needed_response",
            "fail_callcount",
            "cancel_callcount",
            "finish_callcount",
            "expected_result"
        ],
        [
            [
                (False, False, False),
                0,
                0,
                0,
                True
            ],
            [
                (True, False, False),
                1,
                0,
                0,
                False
            ],
            [
                (False, True, False),
                0,
                1,
                0,
                False
            ],
            [
                (False, False, True),
                0,
                0,
                1,
                False
            ],
        ])
    def test_should_continue(
        self,
        mocker,
        check_action_needed_response,
        fail_callcount,
        cancel_callcount,
        finish_callcount,
        expected_result
    ):
        mocked_check_action_needed = mocker.patch(
            "conftest.TestPipelineWithSteps._check_action_needed",
            return_value=check_action_needed_response
        )
        mocked_fail = mocker.patch(
            "conftest.TestPipelineWithSteps.fail",
            return_value=None,
        )
        mocked_cancel = mocker.patch(
            "conftest.TestPipelineWithSteps.cancel",
            return_value=None,
        )
        mocked_finish = mocker.patch(
            "conftest.TestPipelineWithSteps.finish",
            return_value=None,
        )

        instance = TestPipelineWithSteps(repository_class=TestRepository)
        result = instance._should_continue(steps=[])

        mocked_check_action_needed.assert_called_once()
        assert mocked_fail.call_count == fail_callcount
        assert mocked_cancel.call_count == cancel_callcount
        assert mocked_finish.call_count == finish_callcount
        assert result == expected_result
