from abc import ABC, abstractmethod
from typing import List
import cohere  # type: ignore
from typeguard import typechecked
import os


@typechecked
class BaseDenseEmbedder(ABC):
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Embed a single text string"""
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of text strings"""
        pass


@typechecked
class CohereDenseEmbedder(BaseDenseEmbedder):
    def __init__(self, api_key: str, model: str = "embed-english-v3.0"):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Cohere API key must be provided or set in COHERE_API_KEY "
                "environment variable"
            )

        self.client = cohere.Client(self.api_key)
        self.model = model

    async def embed_text(self, text: str) -> List[float]:
        """
        Embed a single text string using Cohere's API
        """
        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type="search_document"
        )
        if isinstance(response.embeddings, list):
            return response.embeddings[0]
        else:
            raise ValueError("Embedding is not a list")

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple texts in a single API call
        """
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type="search_document"
        )
        if isinstance(response.embeddings, list):
            return response.embeddings
        else:
            raise ValueError("Embedding is not a list of lists")
