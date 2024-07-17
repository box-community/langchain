import pytest
from pytest_mock import MockerFixture

from langchain_box.tools import BoxTextRepTool

from langchain_core.documents import Document

from pydantic.v1.error_wrappers import ValidationError

# Test auth types
def test_token_initialization() -> None:
    text_rep_tool = BoxTextRepTool(
        box_developer_token="box_developer_token"
    )
    assert text_rep_tool.box_developer_token == "box_developer_token"
    
def test_failed_token_initialization() -> None:
    with pytest.raises(ValidationError):
        text_rep_tool = BoxTextRepTool()