import pytest
from src.embedders.dense_embedder import CohereDenseEmbedder
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.asyncio
async def test_embed_text() -> None:
    text = "This is a test document"
    embedder = CohereDenseEmbedder(api_key=os.getenv("COHERE_API_KEY"))
    embedding = await embedder.embed_text(text)
    assert isinstance(embedding, list)
    assert all(isinstance(x, float) for x in embedding)
    assert len(embedding) > 0


@pytest.mark.asyncio
async def test_embed_batch() -> None:
    embedder = CohereDenseEmbedder(api_key=os.getenv("COHERE_API_KEY"))
    texts = [
        "This is the first document",
        "This is the second document",
        "This is the third document"
    ]
    embeddings = await embedder.embed_batch(texts)
    assert isinstance(embeddings, list)
    assert len(embeddings) == len(texts)
    assert all(isinstance(x, list) for x in embeddings)
    assert all(isinstance(y, float) for x in embeddings for y in x)
