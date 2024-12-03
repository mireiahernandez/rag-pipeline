# full retriever pipeline
# including embedding the query and then returns only the text
# for the generation part
from abc import ABC, abstractmethod
from typeguard import typechecked
from src.embedders.dense_embedder import BaseDenseEmbedder
from src.retrievers.dense_retriever import BaseDenseRetriever
from typing import List
from src.models import Vector


@typechecked
class BaseRetrieverPipeline(ABC):
    @abstractmethod
    @typechecked
    async def retrieve(self, query: str) -> List[str]:
        pass


@typechecked
class RetrieverPipeline(BaseRetrieverPipeline):
    def __init__(
        self, embedder: BaseDenseEmbedder,
        retriever: BaseDenseRetriever
    ):
        self.embedder = embedder
        self.retriever = retriever

    async def retrieve(self, query: str) -> List[str]:
        query_embedding: List[float] = await self.embedder.embed_text(query)
        results: List[Vector] = await self.retriever.retrieve(query_embedding)
        docs: List[str] = [result.text for result in results]
        return docs
