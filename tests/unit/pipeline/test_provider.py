import pytest

from conftest import TestRepository

from prorch.dataclasses.pipeline import PipelineData
from prorch.providers.pipeline_provider import PipelineProvider


class TestPipelineProvider:
    @pytest.mark.parametrize(["active_pipelines", "expected_items"], [
        [
            [
                {
                    "uuid": "mocked_1",
                    "name": "mocked_1",
                    "metadata": {},
                    "status": "mocked",
                },
                {
                    "uuid": "mocked_2",
                    "name": "mocked_2",
                    "metadata": {},
                    "status": "mocked",
                },
            ],
            [
                PipelineData(**{
                    "uuid": "mocked_1",
                    "name": "mocked_1",
                    "metadata": {},
                    "status": "mocked",
                }),
                PipelineData(**{
                    "uuid": "mocked_2",
                    "name": "mocked_2",
                    "metadata": {},
                    "status": "mocked",
                })
            ]
        ],
        [
            [], []
        ],
        [
            None, []
        ]
    ])
    def test_get_active_pipelines(
        self,
        mocker,
        active_pipelines,
        expected_items,
    ):
        mocked_provider_search = mocker.patch(
            "conftest.TestRepository.search",
            return_value=active_pipelines,
        )

        provider = PipelineProvider(repository_class=TestRepository)
        result = provider.get_active_pipelines()

        mocked_provider_search.call_once_with(filter=["status", "pending"])
        assert result == expected_items
        assert len(result) == len(expected_items)

    @pytest.mark.parametrize(["pipeline_data", "expected_item"], [
        [
            {
                "uuid": "mocked_1",
                "name": "mocked_1",
                "metadata": {},
                "status": "mocked",
            },
            PipelineData(
                uuid="mocked_1",
                name="mocked_1",
                metadata={},
                status="mocked",
            )
        ],
        [
            None, None
        ]
    ])
    def test_get_pipeline_by_uuid(self, mocker, pipeline_data, expected_item):
        mocked_provider_get = mocker.patch(
            "conftest.TestRepository.get",
            return_value=pipeline_data,
        )

        provider = PipelineProvider(repository_class=TestRepository)
        result = provider.get_pipeline_by_uuid(uuid="mocked")

        assert mocked_provider_get.called_once_with(uuid="mocked")
        assert result == expected_item
