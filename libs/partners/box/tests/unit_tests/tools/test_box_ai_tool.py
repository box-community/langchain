import pytest
from pytest_mock import MockerFixture

from langchain_box.tools import BoxAIAskTool

from langchain_core.documents import Document

from pydantic.v1.error_wrappers import ValidationError

# Test auth types
def test_token_initialization() -> None:
    ai_tool = BoxAIAskTool(
        box_developer_token="box_developer_token",
        box_file_ids=["box_file_ids"]
    )
    assert ai_tool.box_developer_token == "box_developer_token"
    assert ai_tool.box_file_ids == ["box_file_ids"]
    
def test_failed_token_initialization() -> None:
    with pytest.raises(ValidationError):
        ai_tool = BoxAIAskTool()