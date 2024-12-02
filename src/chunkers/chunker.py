# 2. Chunker
from abc import ABC, abstractmethod


# Abstract class for chunking text
class BaseChunker(ABC):
    @abstractmethod
    def chunk_text(self, text: str, chunk_size: int = 500) -> list:
        pass


class UniformChunker(BaseChunker):
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500) -> list:
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
