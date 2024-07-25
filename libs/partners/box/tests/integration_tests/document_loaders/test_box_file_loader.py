import pytest
from pytest_mock import MockerFixture

from langchain_box.document_loaders.box_files import BoxFileLoader
from langchain_box.utilities.box_auth import BoxAuthType

from langchain_core.documents import Document


# test Document retrieval
def test_file_load(mocker: MockerFixture) -> None:
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_document_by_file_id", return_value=[]
    )

    loader = BoxFileLoader(
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=["box_file_ids"],
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

    loader = BoxFileLoader(
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=["box_file_ids"],
    )

    documents = loader.load()
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents",
            metadata={"title": "Testing Files"},
        )
    ]
