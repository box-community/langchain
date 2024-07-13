import os
from typing import Any
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockerFixture

from libs.partners.box.langchain_box.document_loaders.box import BoxLoader, Mode
from libs.partners.box.langchain_box.utilities.box import BoxAPIWrapper, BoxAuthType

from langchain_core.documents import Document

from pydantic.v1.error_wrappers import ValidationError

# Test auth types
def test_token_initialization() -> None:
    loader = BoxLoader(
        mode=Mode.FILES,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=['123456789']
    )
    assert loader.mode == "files"
    assert loader.auth_type == "token"
    assert loader.box_developer_token == "box_developer_token"
    assert loader.box_file_ids == ['123456789']

def test_failed_token_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxLoader(
            mode=Mode.FILES,
            auth_type=BoxAuthType.TOKEN,
            box_file_ids=['123456789']
        )

def test_jwt_eid_initialization() -> None:
    loader = BoxLoader(
        mode=Mode.FILES,
        auth_type=BoxAuthType.JWT,
        box_jwt_path="box_jwt_path",
        box_file_ids=['123456789']
    )
    assert loader.mode == "files"
    assert loader.auth_type == "jwt"
    assert loader.box_jwt_path == "box_jwt_path"
    assert loader.box_file_ids == ['123456789']

def test_jwt_user_initialization() -> None:
    loader = BoxLoader(
        mode=Mode.FILES,
        auth_type=BoxAuthType.JWT,
        box_jwt_path="box_jwt_path",
        box_user_id="987654321",
        box_file_ids=['123456789']
    )
    assert loader.mode == "files"
    assert loader.auth_type == "jwt"
    assert loader.box_jwt_path == "box_jwt_path"
    assert loader.box_user_id == "987654321"
    assert loader.box_file_ids == ['123456789']

def test_failed_jwt_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxLoader(
            mode=Mode.FILES,
            auth_type=BoxAuthType.JWT,
            box_file_ids=['123456789']
        )

def test_ccg_eid_initialization() -> None:
    loader = BoxLoader(
        mode=Mode.FILES,
        auth_type=BoxAuthType.CCG,
        box_client_id="box_client_id",
        box_client_secret="box_client_secret",
        box_enterprise_id="box_enterprise_id",
        box_file_ids=['123456789']
    )
    assert loader.mode == "files"
    assert loader.auth_type == "ccg"
    assert loader.box_client_id == "box_client_id"
    assert loader.box_client_secret == "box_client_secret"
    assert loader.box_enterprise_id == "box_enterprise_id"
    assert loader.box_file_ids == ['123456789']

def test_ccg_user_initialization() -> None:
    loader = BoxLoader(
        mode=Mode.FILES,
        auth_type=BoxAuthType.CCG,
        box_client_id="box_client_id",
        box_client_secret="box_client_secret",
        box_enterprise_id="box_enterprise_id",
        box_user_id="987654321",
        box_file_ids=['123456789']
    )
    assert loader.mode == "files"
    assert loader.auth_type == "ccg"
    assert loader.box_client_id == "box_client_id"
    assert loader.box_client_secret == "box_client_secret"
    assert loader.box_enterprise_id == "box_enterprise_id"
    assert loader.box_user_id == "987654321"
    assert loader.box_file_ids == ['123456789']

def test_failed_ccg_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxLoader(
            mode=Mode.FILES,
            auth_type=BoxAuthType.CCG,
            box_enterprise_id="box_enterprise_id",
            box_user_id="987654321",
            box_file_ids=['123456789']
        )

# test modes
def test_files_initialization():
    loader = BoxLoader(
        mode=Mode.FILES,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=['123456789']
    )
    assert loader.mode == "files"
    assert loader.auth_type == "token"
    assert loader.box_developer_token == "box_developer_token"
    assert loader.box_file_ids == ['123456789']

def test_failed_file_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxLoader(
            mode=Mode.FILES,
            auth_type=BoxAuthType.TOKEN,
            box_developer_token="box_developer_token"
        )

def test_folder_initialization():
    loader = BoxLoader(
        mode=Mode.FOLDER,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_folder_id="123456789"
    )
    assert loader.mode == "folder"
    assert loader.auth_type == "token"
    assert loader.box_developer_token == "box_developer_token"
    assert loader.box_folder_id == "123456789"

def test_failed_folder_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxLoader(
            mode=Mode.FOLDER,
            auth_type=BoxAuthType.TOKEN,
            box_developer_token="box_developer_token"
        )

def test_search_initialization(): 
    loader = BoxLoader(
        mode=Mode.SEARCH,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_search_query="box_search_query"
    )
    assert loader.mode == "search"
    assert loader.auth_type == "token"
    assert loader.box_developer_token == "box_developer_token"
    assert loader.box_search_query == "box_search_query"

def test_failed_search_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxLoader(
            mode=Mode.SEARCH,
            auth_type=BoxAuthType.TOKEN,
            box_developer_token="box_developer_token"
        )

def test_metadata_query_initialization():
    loader = BoxLoader(
        mode=Mode.METADATA_QUERY,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_metadata_query="box_metadata_query",
        box_metadata_template="box_metadata_template",
        box_metadata_params="box_metadata_params"
    )
    assert loader.mode == "metadata_query"
    assert loader.auth_type == "token"
    assert loader.box_developer_token == "box_developer_token"
    assert loader.box_metadata_query == "box_metadata_query"
    assert loader.box_metadata_template == "box_metadata_template"
    assert loader.box_metadata_params == "box_metadata_params"

def test_failed_metadata_query_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxLoader(
            mode=Mode.METADATA_QUERY,
            auth_type=BoxAuthType.TOKEN,
            box_developer_token="box_developer_token"
        )

def test_ai_ask_initialization():
    loader = BoxLoader(
        mode=Mode.BOX_AI_ASK,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=['123456789'],
        box_ai_prompt="box_ai_prompt"
    )
    assert loader.mode == "box_ai_ask"
    assert loader.auth_type == "token"
    assert loader.box_developer_token == "box_developer_token"
    assert loader.box_file_ids == ['123456789']
    assert loader.box_ai_prompt == "box_ai_prompt"

def test_failed_metadata_query_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxLoader(
            mode=Mode.BOX_AI_ASK,
            auth_type=BoxAuthType.TOKEN,
            box_developer_token="box_developer_token"
        )

# test Document retrieval
def test_file_load(mocker: MockerFixture) -> None:
    
    mocker.patch(
        "langchain_community.utilities.box.BoxAPIWrapper.get_documents_by_file_ids", 
        return_value=[]
    )

    loader = BoxLoader(
        mode=Mode.FILES,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=['123456789']
    )
    
    documents = loader.load()
    assert documents == []

    mocker.patch(
        "langchain_community.utilities.box.BoxAPIWrapper.get_documents_by_file_ids",
        return_value=(
            [Document(page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"})]
        ),
    )

    loader = BoxLoader(
        mode=Mode.FILES,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=['123456789']
    )

    documents = loader.load()
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"}
        )
    ]

def test_folder_load(mocker: MockerFixture) -> None:
    
    mocker.patch(
        "langchain_community.utilities.box.BoxAPIWrapper.get_documents_by_folder_id", 
        return_value=[]
    )

    loader = BoxLoader(
        mode=Mode.FOLDER,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_folder_id="123456789"
    )
    
    documents = loader.load()
    assert documents == []

    mocker.patch(
        "langchain_community.utilities.box.BoxAPIWrapper.get_documents_by_folder_id",
        return_value=(
            [Document(page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"})]
        ),
    )

    loader = BoxLoader(
        mode=Mode.FOLDER,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_folder_id="123456789"
    )

    documents = loader.load()
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"}
        )
    ]

def test_search_load(mocker: MockerFixture) -> None:
    
    mocker.patch(
        "langchain_community.utilities.box.BoxAPIWrapper.get_documents_by_search", 
        return_value=[]
    )

    loader = BoxLoader(
        mode=Mode.SEARCH,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_search_query="box_search_query"
    )
    
    documents = loader.load()
    assert documents == []

    mocker.patch(
        "langchain_community.utilities.box.BoxAPIWrapper.get_documents_by_search",
        return_value=(
            [Document(page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"})]
        ),
    )

    loader = BoxLoader(
        mode=Mode.SEARCH,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_search_query="box_search_query"
    )

    documents = loader.load()
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"}
        )
    ]

def test_metadata_query_load(mocker: MockerFixture) -> None:
    
    mocker.patch(
        "langchain_community.utilities.box.BoxAPIWrapper.get_documents_by_metadata_query", 
        return_value=[]
    )

    loader = BoxLoader(
        mode=Mode.METADATA_QUERY,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_metadata_query="box_metadata_query",
        box_metadata_template="box_metadata_template",
        box_metadata_params="box_metadata_params"
    )
    
    documents = loader.load()
    assert documents == []

    mocker.patch(
        "langchain_community.utilities.box.BoxAPIWrapper.get_documents_by_metadata_query",
        return_value=(
            [Document(page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"})]
        ),
    )

    loader = BoxLoader(
        mode=Mode.METADATA_QUERY,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_metadata_query="box_metadata_query",
        box_metadata_template="box_metadata_template",
        box_metadata_params="box_metadata_params"
    )

    documents = loader.load()
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"}
        )
    ]

def test_box_ai_load(mocker: MockerFixture) -> None:
    
    mocker.patch(
        "langchain_community.utilities.box.BoxAPIWrapper.get_documents_by_box_ai_ask", 
        return_value=[]
    )
    
    loader = BoxLoader(
        mode=Mode.BOX_AI_ASK,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=['123456789'],
        box_ai_prompt="box_ai_prompt"
    )
    
    documents = loader.load()
    assert documents == []

    mocker.patch(
        "langchain_community.utilities.box.BoxAPIWrapper.get_documents_by_box_ai_ask",
        return_value=(
            [Document(page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"})]
        ),
    )
    
    loader = BoxLoader(
        mode=Mode.BOX_AI_ASK,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=['123456789'],
        box_ai_prompt="box_ai_prompt"
    )

    documents = loader.load()
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"}
        )
    ]