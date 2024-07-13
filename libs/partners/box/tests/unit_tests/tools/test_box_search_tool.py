import os
from typing import Any
from unittest.mock import Mock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockerFixture

from langchain_box.tools import BoxFileSearchTool
from langchain_box.utilities import BoxAPIWrapper, BoxAuthType

from langchain_core.documents import Document

from pydantic.v1.error_wrappers import ValidationError

# Test auth types
def test_token_initialization() -> None:
    search_tool = BoxFileSearchTool(
        box_developer_token="box_developer_token"
    )
    assert search_tool.box_developer_token == "box_developer_token"
    
def test_failed_token_initialization() -> None:
    with pytest.raises(ValidationError):
        search_tool = BoxFileSearchTool()

def test_search_load(mocker: MockerFixture) -> None:
    
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_documents_by_search", 
        return_value=[]
    )

    search_tool = BoxFileSearchTool(
        box_developer_token="box_developer_token"
    )
    
    documents = search_tool._run("query")
    assert documents == []

    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_documents_by_search",
        return_value=(
            [Document(page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"})]
        ),
    )

    documents = search_tool._run("query")
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"}
        )
    ]