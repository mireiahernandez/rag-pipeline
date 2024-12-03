from src.chunkers.chunker import ApproximateChunkerWithOverlap
from src.models import Metadata
import pytest


@pytest.mark.asyncio
async def test_approximate_chunker_with_overlap_long_text():
    chunker = ApproximateChunkerWithOverlap(
        chunk_size=512,
        chunk_overlap=128,
    )
    text = "This is a test text"*1000
    metadata = Metadata(
        title="Test Title",
        author="Test Author",
        description="Test Subject",
        keywords=["test", "chunker"],
        created_at="2024-01-01"
    )
    chunks = await chunker.chunk_text(text, metadata)
    assert len(chunks) == 14
    title = "Title: Test Title\nAuthor: Test Author\nDescription: Test Subject\n\n" # noqa E501
    assert title in chunks[0]
    assert "This is a test text" in chunks[0]


@pytest.mark.asyncio
async def test_approximate_chunker_with_overlap_short_text():
    chunker = ApproximateChunkerWithOverlap(
        chunk_size=512,
        chunk_overlap=128,
    )
    text = "This is a test text"
    metadata = Metadata(
        title="Test Title",
        author="Test Author",
        description="Test Subject",
        keywords=["test", "chunker"],
        created_at="2024-01-01"
    )
    chunks = await chunker.chunk_text(text, metadata)
    assert len(chunks) == 1
