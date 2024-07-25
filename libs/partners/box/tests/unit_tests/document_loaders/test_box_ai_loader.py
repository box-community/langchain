import pytest
from pytest_mock import MockerFixture

from langchain_box.document_loaders import BoxAILoader, BoxAIMode
from langchain_box.utilities import BoxAuthType

from langchain_core.documents import Document

from pydantic.v1.error_wrappers import ValidationError


# Test auth types
def test_token_initialization() -> None:
    loader = BoxAILoader(
        mode=BoxAIMode.ASK,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=["box_file_ids"],
        box_ai_prompt="box_ai_prompt",
    )
    assert loader.mode == "ask"
    assert loader.auth_type == "token"
    assert loader.box_developer_token == "box_developer_token"
    assert loader.box_file_ids == ["box_file_ids"]
    assert loader.box_ai_prompt == "box_ai_prompt"


def test_failed_token_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxAILoader(
            mode=BoxAIMode.ASK,
            auth_type=BoxAuthType.TOKEN,
            box_file_ids=["box_file_ids"],
            box_ai_prompt="box_ai_prompt",
        )


def test_jwt_eid_initialization() -> None:
    loader = BoxAILoader(
        mode=BoxAIMode.ASK,
        auth_type=BoxAuthType.JWT,
        box_jwt_path="box_jwt_path",
        box_file_ids=["box_file_ids"],
        box_ai_prompt="box_ai_prompt",
    )
    assert loader.mode == "ask"
    assert loader.auth_type == "jwt"
    assert loader.box_jwt_path == "box_jwt_path"
    assert loader.box_file_ids == ["box_file_ids"]
    assert loader.box_ai_prompt == "box_ai_prompt"


def test_jwt_user_initialization() -> None:
    loader = BoxAILoader(
        mode=BoxAIMode.ASK,
        auth_type=BoxAuthType.JWT,
        box_jwt_path="box_jwt_path",
        box_user_id="box_user_id",
        box_file_ids=["box_file_ids"],
        box_ai_prompt="box_ai_prompt",
    )
    assert loader.mode == "ask"
    assert loader.auth_type == "jwt"
    assert loader.box_jwt_path == "box_jwt_path"
    assert loader.box_user_id == "box_user_id"
    assert loader.box_file_ids == ["box_file_ids"]
    assert loader.box_ai_prompt == "box_ai_prompt"


def test_failed_jwt_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxAILoader(
            mode=BoxAIMode.ASK,
            auth_type=BoxAuthType.JWT,
            box_file_ids=["box_file_ids"],
            box_ai_prompt="box_ai_prompt",
        )


def test_ccg_eid_initialization() -> None:
    loader = BoxAILoader(
        mode=BoxAIMode.ASK,
        auth_type=BoxAuthType.CCG,
        box_client_id="box_client_id",
        box_client_secret="box_client_secret",
        box_enterprise_id="box_enterprise_id",
        box_file_ids=["box_file_ids"],
        box_ai_prompt="box_ai_prompt",
    )
    assert loader.mode == "ask"
    assert loader.auth_type == "ccg"
    assert loader.box_client_id == "box_client_id"
    assert loader.box_client_secret == "box_client_secret"
    assert loader.box_enterprise_id == "box_enterprise_id"
    assert loader.box_file_ids == ["box_file_ids"]
    assert loader.box_ai_prompt == "box_ai_prompt"


def test_ccg_user_initialization() -> None:
    loader = BoxAILoader(
        mode=BoxAIMode.ASK,
        auth_type=BoxAuthType.CCG,
        box_client_id="box_client_id",
        box_client_secret="box_client_secret",
        box_enterprise_id="box_enterprise_id",
        box_user_id="box_user_id",
        box_file_ids=["box_file_ids"],
        box_ai_prompt="box_ai_prompt",
    )
    assert loader.mode == "ask"
    assert loader.auth_type == "ccg"
    assert loader.box_client_id == "box_client_id"
    assert loader.box_client_secret == "box_client_secret"
    assert loader.box_enterprise_id == "box_enterprise_id"
    assert loader.box_user_id == "box_user_id"
    assert loader.box_file_ids == ["box_file_ids"]
    assert loader.box_ai_prompt == "box_ai_prompt"


def test_failed_ccg_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxAILoader(
            mode=BoxAIMode.ASK,
            auth_type=BoxAuthType.CCG,
            box_enterprise_id="box_enterprise_id",
            box_user_id="box_user_id",
            box_file_ids=["box_file_ids"],
            box_ai_prompt="box_ai_prompt",
        )


def test_failed_metadata_query_initialization() -> None:
    with pytest.raises(ValidationError):
        loader = BoxAILoader(
            mode=BoxAIMode.ASK,
            auth_type=BoxAuthType.TOKEN,
            box_developer_token="box_developer_token",
        )
