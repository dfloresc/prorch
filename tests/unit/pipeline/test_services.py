import pytest

from prorch.dataclasses.pipeline import PipelineData
from prorch.pipeline.services import get_active_pipelines
from conftest import TestRepository


class TestPipelineServices:
    def test_get_active_pipelines_should_call_repository(self, mocker):
        mocked_provider_get_active_pipelines = mocker.patch(
            "prorch.pipeline.services.PipelineProvider.get_active_pipelines",  # noqa: E501
            return_value=[],
        )

        get_active_pipelines(repository_class=TestRepository)

        mocked_provider_get_active_pipelines.assert_called_once()

    @pytest.mark.parametrize(["active_pipelines", "count"], [
        [
            [
                PipelineData(
                    uuid="mocked_1",
                    name="mocked_1",
                    metadata={},
                    status="mocked",
                ),
                PipelineData(
                    uuid="mocked_2",
                    name="mocked_2",
                    metadata={},
                    status="mocked",
                ),
            ],
            2
        ],
        [
            [], 0
        ]
    ])
    def test_get_active_pipelines_should_return_a_value(
        self,
        mocker,
        active_pipelines,
        count,
    ):
        mocked_active_pipeline = active_pipelines
        mocked_provider_get_active_pipelines = mocker.patch(
            "prorch.pipeline.services.PipelineProvider.get_active_pipelines",  # noqa: E501
            return_value=mocked_active_pipeline,
        )

        result = get_active_pipelines(repository_class=TestRepository)

        mocked_provider_get_active_pipelines.called_once()
        assert len(result) == count
