import pytest
from pytest_mock import MockerFixture

from box_sdk_gen import FileFull

from langchain_box.document_loaders.box_folder import BoxFolderLoader
from langchain_box.utilities.box_auth import BoxAuthType

from langchain_core.documents import Document

def test_folder_load(mocker: MockerFixture) -> None:

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
        return_value=file_list
    )
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_document_by_file_id", 
        return_value=[]
    )

    loader = BoxFolderLoader(
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_folder_id="box_folder_id"
    )
    
    documents = loader.load()
    assert documents

    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_document_by_file_id",
        return_value=(
            Document(page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"})
        ),
    )

    loader = BoxFolderLoader(
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_folder_id="box_folder_id"
    )

    documents = loader.load()
    print(f"documents {documents}")
    assert documents == ([
        Document(
            page_content="Test file mode\ndocument contents", metadata={"title": "Testing Files"}
        )
    ])