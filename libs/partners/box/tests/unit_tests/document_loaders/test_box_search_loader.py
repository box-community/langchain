import pytest
from pytest_mock import MockerFixture

from langchain_box.document_loaders.box_search import BoxSearchLoader
from langchain_box.utilities.box_auth import BoxAuthType

from langchain_core.documents import Document

from pydantic.v1.error_wrappers import ValidationError

# Test auth types
def test_token_initialization() -> None:
    loader = BoxSearchLoader(
        
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_search_query="box_search_query"
    )
    
    assert loader.auth_type == "token"
    assert loader.box_developer_token == "box_developer_token"
    assert loader.box_search_query == "box_search_query"

def test_failed_token_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxSearchLoader(
            
            auth_type=BoxAuthType.TOKEN,
            box_search_query="box_search_query"
        )

def test_jwt_eid_initialization() -> None:
    loader = BoxSearchLoader(
        
        auth_type=BoxAuthType.JWT,
        box_jwt_path="box_jwt_path",
        box_search_query="box_search_query"
    )
    
    assert loader.auth_type == "jwt"
    assert loader.box_jwt_path == "box_jwt_path"
    assert loader.box_search_query == "box_search_query"

def test_jwt_user_initialization() -> None:
    loader = BoxSearchLoader(
        
        auth_type=BoxAuthType.JWT,
        box_jwt_path="box_jwt_path",
        box_user_id="box_user_id",
        box_search_query="box_search_query"
    )
    
    assert loader.auth_type == "jwt"
    assert loader.box_jwt_path == "box_jwt_path"
    assert loader.box_user_id == "box_user_id"
    assert loader.box_search_query == "box_search_query"

def test_failed_jwt_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxSearchLoader(
            
            auth_type=BoxAuthType.JWT,
            box_search_query="box_search_query"
        )

def test_ccg_eid_initialization() -> None:
    loader = BoxSearchLoader(
        
        auth_type=BoxAuthType.CCG,
        box_client_id="box_client_id",
        box_client_secret="box_client_secret",
        box_enterprise_id="box_enterprise_id",
        box_search_query="box_search_query"
    )
    
    assert loader.auth_type == "ccg"
    assert loader.box_client_id == "box_client_id"
    assert loader.box_client_secret == "box_client_secret"
    assert loader.box_enterprise_id == "box_enterprise_id"
    assert loader.box_search_query == "box_search_query"

def test_ccg_user_initialization() -> None:
    loader = BoxSearchLoader(
        
        auth_type=BoxAuthType.CCG,
        box_client_id="box_client_id",
        box_client_secret="box_client_secret",
        box_enterprise_id="box_enterprise_id",
        box_user_id="box_user_id",
        box_search_query="box_search_query"
    )

    assert loader.auth_type == "ccg"
    assert loader.box_client_id == "box_client_id"
    assert loader.box_client_secret == "box_client_secret"
    assert loader.box_enterprise_id == "box_enterprise_id"
    assert loader.box_user_id == "box_user_id"
    assert loader.box_search_query == "box_search_query"

def test_failed_ccg_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxSearchLoader(
            
            auth_type=BoxAuthType.CCG,
            box_enterprise_id="box_enterprise_id",
            box_user_id="box_user_id",
            box_search_query="box_search_query"
        )

def test_failed_search_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxSearchLoader(
            
            auth_type=BoxAuthType.TOKEN,
            box_developer_token="box_developer_token"
        )

def test_search_load(mocker: MockerFixture) -> None:
    
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_search_results", 
        return_value=["id"]
    )
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_document_by_file_id", 
        return_value=[]
    )

    loader = BoxSearchLoader(
        
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_search_query="box_search_query"
    )
    
    documents = loader.load()
    assert documents

    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_document_by_file_id",
        return_value=(
            Document(page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"})
        ),
    )

    loader = BoxSearchLoader(
        
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