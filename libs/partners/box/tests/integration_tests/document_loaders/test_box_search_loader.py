import pytest
from pytest_mock import MockerFixture

from langchain_box.document_loaders.box_search import BoxSearchLoader
from langchain_box.utilities.box_auth import BoxAuthType

from langchain_core.documents import Document


def test_search_load(mocker: MockerFixture) -> None:
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_search_results", return_value=["id"]
    )
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_document_by_file_id", return_value=[]
    )

    loader = BoxSearchLoader(
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_search_query="box_search_query",
    )

    documents = loader.load()
    assert documents

    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_document_by_file_id",
        return_value=(
            Document(
                page_content="Test file mode\ndocument contents",
                metadata={"title": "Testing Files"},
            )
        ),
    )

    loader = BoxSearchLoader(
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_search_query="box_search_query",
    )

    documents = loader.load()
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents",
            metadata={"title": "Testing Files"},
        )
    ]
