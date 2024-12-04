# implement dense retriever
from abc import ABC, abstractmethod
from typing import List
from typeguard import typechecked
from motor.motor_asyncio import AsyncIOMotorCollection
from src.models import Vector
from typing import Sequence, Mapping, Any


@typechecked
class BaseDenseRetriever(ABC):
    vector_collection: AsyncIOMotorCollection

    @abstractmethod
    @typechecked
    async def retrieve(
        self,
        query_embedding: List[float],
        k: int = 10
    ) -> List[Vector]:
        pass


@typechecked
@typechecked
class NNRetriever(BaseDenseRetriever):
    def __init__(self, vector_collection: AsyncIOMotorCollection):
        self.vector_collection = vector_collection

    @typechecked
    async def retrieve(
        self,
        query_embedding: List[float],
        k: int = 10
    ) -> List[Vector]:
        """
        Retrieve the IDs and cosine similarity of the top k
        most similar documents
        """
        pipeline: Sequence[Mapping[str, Any]] = [
            {
                "$project": {
                    "parent_id": 1,
                    "vector_embedding": 1,
                    "vector_id": 1,
                    "metadata": 1,
                    "text": 1,
                    "cosineSimilarity": {
                        "$divide": [
                            {"$reduce": {
                                "input": {"$zip": {"inputs": ["$vector_embedding", query_embedding]}},  # noqa: E501
                                "initialValue": 0,
                                "in": {"$add": ["$$value", {"$multiply": [{"$arrayElemAt": ["$$this", 0]}, {"$arrayElemAt": ["$$this", 1]}]}]}  # noqa: E501
                            }},
                            {
                                "$multiply": [
                                    {"$sqrt": {"$reduce": {
                                        "input": "$vector_embedding",
                                        "initialValue": 0,
                                        "in": {"$add": ["$$value", {"$multiply": ["$$this", "$$this"]}]}  # noqa: E501
                                    }}},
                                    {"$sqrt": {"$reduce": {
                                        "input": query_embedding,
                                        "initialValue": 0,
                                        "in": {"$add": ["$$value", {"$multiply": ["$$this", "$$this"]}]}  # noqa: E501
                                    }}}
                                ]
                            }
                        ]
                    }
                }
            },
            {"$sort": {"cosineSimilarity": -1}},
            {"$limit": k},
            {"$project": {
                "parent_id": 1,
                "cosineSimilarity": 1,
                "_id": 1,
                "vector_embedding": 1,
                "vector_id": 1,
                "text": 1,
                "metadata": 1
            }}
        ]

        # Execute the aggregation pipeline
        results = []
        async for doc in self.vector_collection.aggregate(pipeline):
            vector = Vector(
                vector_embedding=doc["vector_embedding"],
                vector_id=doc["vector_id"],
                text=doc["text"],
                metadata=doc["metadata"],
                parent_id=doc["parent_id"]
            )
            results.append(vector)
        return results
