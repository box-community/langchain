import pytest
from pytest_mock import MockerFixture

from langchain_box.document_loaders.box_metadata_query import BoxMetadataQueryLoader
from langchain_box.utilities.box_auth import BoxAuthType

from langchain_core.documents import Document


def test_metadata_query_load(mocker: MockerFixture) -> None:
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_metadata_query_results",
        return_value=["id"],
    )
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_document_by_file_id", return_value=[]
    )

    loader = BoxMetadataQueryLoader(
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_metadata_query="box_metadata_query",
        box_metadata_template="box_metadata_template",
        box_metadata_params="box_metadata_params",
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

    loader = BoxMetadataQueryLoader(
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_metadata_query="box_metadata_query",
        box_metadata_template="box_metadata_template",
        box_metadata_params="box_metadata_params",
    )

    documents = loader.load()
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents",
            metadata={"title": "Testing Files"},
        )
    ]
