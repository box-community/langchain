"""Test Box embeddings."""
from langchain_box.embeddings import BoxEmbeddings


def test_langchain_box_embedding_documents() -> None:
    """Test cohere embeddings."""
    documents = ["foo bar"]
    embedding = BoxEmbeddings()
    output = embedding.embed_documents(documents)
    assert len(output) == 1
    assert len(output[0]) > 0


def test_langchain_box_embedding_query() -> None:
    """Test cohere embeddings."""
    document = "foo bar"
    embedding = BoxEmbeddings()
    output = embedding.embed_query(document)
    assert len(output) > 0
