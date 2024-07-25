import pytest
from pytest_mock import MockerFixture

from langchain_box.tools import BoxFolderContentsTool
from langchain_box.utilities import BoxAPIWrapper

from langchain_core.documents import Document

from pydantic.v1.error_wrappers import ValidationError


# Test auth types
def test_token_initialization() -> None:
    folder_tool = BoxFolderContentsTool(box_developer_token="box_developer_token")
    assert folder_tool.box_developer_token == "box_developer_token"


def test_failed_token_initialization() -> None:
    with pytest.raises(ValidationError):
        folder_tool = BoxFolderContentsTool()
