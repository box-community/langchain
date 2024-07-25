import pytest
from pytest_mock import MockerFixture

from langchain_box.tools import BoxTextRepTool

from langchain_core.documents import Document

from pydantic.v1.error_wrappers import ValidationError

def test_text_rep_load(mocker: MockerFixture) -> None:
    
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_text_representation", 
        return_value=[]
    )

    text_rep_tool = BoxTextRepTool(
        box_developer_token="box_developer_token"
    )
    
    documents = text_rep_tool._run("query")
    assert documents == []

    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_text_representation",
        return_value=(
            [Document(page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"})]
        ),
    )

    documents = text_rep_tool._run("query")
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"}
        )
    ]