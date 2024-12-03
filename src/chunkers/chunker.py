# 2. Chunker
from abc import ABC, abstractmethod
from typing import List
from typeguard import typechecked
from src.models import Metadata


# Abstract class for chunking text
@typechecked
class BaseChunker(ABC):
    @abstractmethod
    @typechecked
    async def chunk_text(self, text: str, metadata: Metadata) -> List[str]:
        pass


@typechecked
class SimpleChunker(BaseChunker):
    @typechecked
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size

    @typechecked
    async def chunk_text(self, text: str, metadata: Metadata) -> List[str]:
        return [text[i:i + self.chunk_size]
                for i in range(0, len(text), self.chunk_size)]


@typechecked
class ApproximateChunkerWithOverlap(BaseChunker):
    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 0,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # use word to token conversion rate to approximate the number of words
        # to avoid using more expensive tokenization
        self.word_to_token_conversion_rate = 0.75

    async def _approximate_split_text(self, text: str) -> List[str]:
        """
        Splits the text into chunks where each chunk contains
        an approximate number of words.
        chunk_size = 512 -- words_per_chunk = 512*0.75 = 384
        chunk_overlap = 128 -- word_overlap = 128*0.75 = 96
        """
        words_per_chunk = round(
            self.chunk_size * self.word_to_token_conversion_rate)
        words_overlap = round(
            self.chunk_overlap * self.word_to_token_conversion_rate)
        words = text.split()
        # split the text into chunks of words_per_chunk with
        # overlap of words_overlap
        chunks: List[str] = []
        for i in range(0, len(words), words_per_chunk - words_overlap):
            chunk = " ".join(words[i:i + words_per_chunk])
            chunks.append(chunk)
        return chunks

    @typechecked
    async def chunk_text(self, text: str, metadata: Metadata) -> List[str]:
        """
         Uses Cohere tokenizer to chunk text in chunks of chunk_size
         with overlap of chunk_overlap
         Aso enhance chunk text with the metadata following the pattern:
            Title: ...
            Author: ...
            Description: ...
            ...
            {chunk}
         """
        chunks = await self._approximate_split_text(text=text)
        enhanced_chunks = []
        for chunk in chunks:
            enhanced_chunk = (
                f"Title: {metadata.title}\n"
                f"Author: {metadata.author}\n"
                f"Description: {metadata.description}\n\n"
                f"{''.join(chunk)}"
            )
            enhanced_chunks.append(enhanced_chunk)

        return enhanced_chunks
