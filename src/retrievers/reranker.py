from typing import List
from cohere import Client  # Make sure to install the cohere package
from src.models import Vector  # Assuming Vector is your data model for vectors
from abc import ABC, abstractmethod


class BaseReranker(ABC):
    @abstractmethod
    def rerank_responses(
        self, query: str,
        responses: List[Vector],
        num_responses: int = 3
    ) -> List[Vector]:
        pass


class Reranker(BaseReranker):
    def __init__(self, cohere_api_key: str):
        """
        Initialize the Reranker with the Cohere client.

        Args:
            cohere_api_key (str): Your Cohere API key.
        """
        self.co = Client(cohere_api_key)

    def rerank_responses(
        self,
        query: str,
        responses: List[Vector],
        num_responses: int = 3
    ) -> List[Vector]:
        """
        Rerank the given responses based on their relevance to the query.

        Args:
            query (str): The query to evaluate against.
            responses (List[str]): The list of responses to rerank.
            num_responses (int): The number of top responses to return.

        Returns:
            List[str]: The reranked list of responses.
        """
        reranked_responses = self.co.rerank(
            query=query,
            documents=[response.text for response in responses],
            top_n=num_responses,
            model='rerank-english-v3.0',
        )
        vector_indices: List[int] = [
            doc.index for doc in reranked_responses.results
        ]
        vectors: List[Vector] = [
            responses[index] for index in vector_indices
        ]
        return vectors
