# 2. Chunker
from abc import ABC, abstractmethod
from typing import List
from typeguard import typechecked


# Abstract class for chunking text
@typechecked
class BaseChunker(ABC):
    @abstractmethod
    @typechecked
    def chunk_text(self, text: str) -> List[str]:
        pass


@typechecked
class SimpleChunker(BaseChunker):
    @typechecked
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size

    @typechecked
    def chunk_text(self, text: str) -> List[str]:
        return [text[i:i + self.chunk_size]
                for i in range(0, len(text), self.chunk_size)]
