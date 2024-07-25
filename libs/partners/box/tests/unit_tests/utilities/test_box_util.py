import os
from typing import Any, List
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockerFixture

from langchain_box.utilities import BoxAPIWrapper, BoxAuth, BoxAuthType

from langchain_core.documents import Document

from pydantic.v1.error_wrappers import ValidationError


def test_initialization():
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

    assert box.auth_type == "token"
    assert box.box_developer_token == "box_developer_token"
    assert box.box_client_id == "box_client_id"
    assert box.box_client_secret == "box_client_secret"
    assert box.box_user_id == "box_user_id"
    assert box.box_enterprise_id == "box_enterprise_id"
    assert box.box_jwt_path == "box_jwt_path"
    assert box.box_file_id == "box_file_id"
    assert box.box_file_ids == ["box_file_ids"]
    assert box.box_folder_id == "box_folder_id"
    assert box.box_search_query == "box_search_query"
    assert box.box_metadata_query == "box_metadata_query"
    assert box.box_metadata_template == "box_metadata_template"
    assert box.box_metadata_params == "box_metadata_params"
    assert box.box_ai_prompt == "box_ai_prompt"


def test_failed_initialization() -> None:
    with pytest.raises(ValidationError):
        box = BoxAPIWrapper(
            auth_type="token",
            box_developer_token="box_developer_token",
            box_client_id="box_client_id",
            box_client_secret="box_client_secret",
            box_user_id="box_user_id",
            box_enterprise_id="box_enterprise_id",
            box_jwt_path="box_jwt_path",
            box_file_id="box_file_id",
            box_file_ids="box_file_ids",  # Not a valid List
            box_folder_id="box_folder_id",
            box_search_query="box_search_query",
            box_metadata_query="box_metadata_query",
            box_metadata_template="box_metadata_template",
            box_metadata_params="box_metadata_params",
            box_ai_prompt="box_ai_prompt",
        )
