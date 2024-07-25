import pytest
from pytest_mock import MockerFixture

from langchain_box.tools import BoxAIAskTool

from langchain_core.documents import Document


def test_ai_load(mocker: MockerFixture) -> None:
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_documents_by_box_ai_ask",
        return_value=[],
    )

    ai_tool = BoxAIAskTool(
        box_developer_token="box_developer_token", box_file_ids=["box_file_ids"]
    )

    documents = ai_tool._run("query")
    assert documents == []

    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_documents_by_box_ai_ask",
        return_value=(
            [
                Document(
                    page_content="Test file mode\ndocument contents",
                    metadata={"title": "Testing Files"},
                )
            ]
        ),
    )

    documents = ai_tool._run("query")
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents",
            metadata={"title": "Testing Files"},
        )
    ]
