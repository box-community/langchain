from pytest_mock import MockerFixture

from langchain_box.document_loaders import BoxAILoader, BoxAIMode
from langchain_box.utilities import BoxAuthType

from langchain_core.documents import Document


def test_box_ai_load(mocker: MockerFixture) -> None:
    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_documents_by_box_ai_ask",
        return_value=[],
    )

    loader = BoxAILoader(
        mode=BoxAIMode.ASK,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=["123456789"],
        box_ai_prompt="box_ai_prompt",
    )

    documents = loader.load()
    assert documents

    mocker.patch(
        "langchain_box.utilities.BoxAPIWrapper.get_documents_by_box_ai_ask",
        return_value=(
            Document(
                page_content="Test file mode\ndocument contents",
                metadata={"title": "Testing Files"},
            )
        ),
    )

    loader = BoxAILoader(
        mode=BoxAIMode.ASK,
        auth_type=BoxAuthType.TOKEN,
        box_developer_token="box_developer_token",
        box_file_ids=["123456789"],
        box_ai_prompt="box_ai_prompt",
    )

    documents = loader.load()
    assert documents == [
        Document(
            page_content="Test file mode\ndocument contents",
            metadata={"title": "Testing Files"},
        )
    ]
