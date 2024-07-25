import pytest
from pytest_mock import MockerFixture

from box_sdk_gen import FileFull

from langchain_box.tools import BoxFolderContentsTool
from langchain_box.utilities import BoxAPIWrapper

from langchain_core.documents import Document

def test_search_load(mocker: MockerFixture) -> None:
    
    file_list = []
    file_list.append(FileFull(
        type="file",
        id="id"
    ))
    file_list.append(FileFull(
        type="folder",
        id="id"
    ))

    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_folder_items", 
        return_value=[]
    )

    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_document_by_file_id",
        return_value=[]
    )

    folder_tool = BoxFolderContentsTool(
        box_developer_token="box_developer_token",
    )
    
    documents = folder_tool._run("query")
    assert documents == []

    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_folder_items",
        return_value=file_list,
    )
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_document_by_file_id",
        return_value=Document(
                page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"}
            )
    )
    print(f"mocker {mocker}")
    documents = folder_tool._run("query")
    print(f"documents {documents}")
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"}
        )
    ]