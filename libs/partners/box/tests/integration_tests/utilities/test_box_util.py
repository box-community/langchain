from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from langchain_box.utilities import BoxAPIWrapper

from langchain_core.documents import Document


@pytest.fixture()
def mock_worker(mocker: MockerFixture):
    mocker.patch("langchain_box.utilities.BoxAuth.authorize", return_value=Mock())
    mocker.patch("langchain_box.utilities.BoxAuth.get_client", return_value=Mock())
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_text_representation",
        return_value=("filename", "content", "url"),
    )


def test_get_documents_by_file_ids(mock_worker) -> None:
    box = BoxAPIWrapper(
        auth_type="token",
        box_developer_token="box_developer_token",
        box_client_id="box_client_id",
        box_client_secret="box_client_secret",
        box_user_id="box_user_id",
        box_enterprise_id="box_enterprise_id",
        box_jwt_path="box_jwt_path",
        box_file_id="box_file_id",
        box_file_ids=["box_file_ids"],
        box_folder_id="box_folder_id",
        box_search_query="box_search_query",
        box_metadata_query="box_metadata_query",
        box_metadata_template="box_metadata_template",
        box_metadata_params="box_metadata_params",
        box_ai_prompt="box_ai_prompt",
    )

    documents = box.get_documents_by_file_ids(["box_file_id"])
    assert documents == [
        Document(
            page_content="content", metadata={"source": "url", "title": "filename"}
        )
    ]


def test_get_documents_by_folder_id(mock_worker, mocker: MockerFixture) -> None:
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_folder_items",
        return_value=([{"id": "file_id", "type": "file"}]),
    )

    box = BoxAPIWrapper(
        auth_type="token",
        box_developer_token="box_developer_token",
        box_client_id="box_client_id",
        box_client_secret="box_client_secret",
        box_user_id="box_user_id",
        box_enterprise_id="box_enterprise_id",
        box_jwt_path="box_jwt_path",
        box_file_id="box_file_id",
        box_file_ids=["box_file_ids"],
        box_folder_id="box_folder_id",
        box_search_query="box_search_query",
        box_metadata_query="box_metadata_query",
        box_metadata_template="box_metadata_template",
        box_metadata_params="box_metadata_params",
        box_ai_prompt="box_ai_prompt",
    )

    folder_contents = box.get_documents_by_folder_id("box_folder_id")
    assert folder_contents == [{"id": "file_id", "type": "file"}]


def test_documents_by_search(mock_worker, mocker: MockerFixture) -> None:
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_search_results",
        return_value=(["file_id"]),
    )

    box = BoxAPIWrapper(
        auth_type="token",
        box_developer_token="box_developer_token",
        box_client_id="box_client_id",
        box_client_secret="box_client_secret",
        box_user_id="box_user_id",
        box_enterprise_id="box_enterprise_id",
        box_jwt_path="box_jwt_path",
        box_file_id="box_file_id",
        box_file_ids=["box_file_ids"],
        box_folder_id="box_folder_id",
        box_search_query="box_search_query",
        box_metadata_query="box_metadata_query",
        box_metadata_template="box_metadata_template",
        box_metadata_params="box_metadata_params",
        box_ai_prompt="box_ai_prompt",
    )

    documents = box.get_documents_by_search("query")
    assert documents == [
        Document(
            page_content="content", metadata={"source": "url", "title": "filename"}
        )
    ]


def test_get_documents_by_metadata_query(mock_worker, mocker: MockerFixture) -> None:
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_metadata_query_results",
        return_value=(["file_id"]),
    )

    box = BoxAPIWrapper(
        auth_type="token",
        box_developer_token="box_developer_token",
        box_client_id="box_client_id",
        box_client_secret="box_client_secret",
        box_user_id="box_user_id",
        box_enterprise_id="box_enterprise_id",
        box_jwt_path="box_jwt_path",
        box_file_id="box_file_id",
        box_file_ids=["box_file_ids"],
        box_folder_id="box_folder_id",
        box_search_query="box_search_query",
        box_metadata_query="box_metadata_query",
        box_metadata_template="box_metadata_template",
        box_metadata_params="box_metadata_params",
        box_ai_prompt="box_ai_prompt",
    )

    documents = box.get_documents_by_metadata_query()
    assert documents == [
        Document(
            page_content="content", metadata={"source": "url", "title": "filename"}
        )
    ]
