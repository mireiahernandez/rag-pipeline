# test knn retriever
import pytest
from src.retrievers.dense_retriever import NNRetriever
import motor
from src.database_handlers.database_handler import MongoDBHandler
import os
from dotenv import load_dotenv
import numpy as np
from src.models import Vector, Metadata


load_dotenv()


@pytest.fixture
def mongodb_client():
    # connect to the local mongodb instance
    mongodb_local_uri = "mongodb://0.0.0.0:" + os.getenv("MONGO_DB_PORT")
    client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_local_uri)
    yield client
    client.close()


@pytest.fixture
def mongodb_handler(mongodb_client):
    db_name = "test_retrieval_db"
    vector_collection_name = "vectors"
    doc_collection_name = "documents"
    return MongoDBHandler(
        mongodb_client,
        db_name,
        doc_collection_name=doc_collection_name,
        vector_collection_name=vector_collection_name
    )


@pytest.fixture
def vector_collection(mongodb_handler):
    return mongodb_handler.vector_collection


@pytest.fixture
def nn_retriever(mongodb_handler):
    return NNRetriever(mongodb_handler.vector_collection)


@pytest.mark.asyncio
async def test_nn_retriever(vector_collection, nn_retriever) -> None:
    # populate a vector collection
    await vector_collection.delete_many({})
    # add 100 vectors to the collection
    for i in range(10):
        vector = Vector(
            vector_embedding=np.random.rand(1536).tolist(),
            text=f"test {i}",
            metadata=Metadata(
                title=f"test {i}",
                author=f"test {i}",
                description=f"test {i}",
                keywords=[f"test {i}"],
                created_at=""
            ),
            parent_id=""
        )

        await vector_collection.insert_one(vector.model_dump())

    query_embedding = np.random.rand(1536).tolist()
    results = await nn_retriever.retrieve(query_embedding)
    assert len(results) == 10

    # delete the vectors
    await vector_collection.delete_many({})


# dummy test to verify that the vectors are sorted by cosine similarity
@pytest.mark.asyncio
async def test_cosine_similarity(vector_collection, nn_retriever) -> None:
    await vector_collection.delete_many({})

    # add 4 vectors with clear different cosine similarity
    embeddings = [
        np.array([1, 0, 0, 0]).tolist(),
        np.array([0, 1, 0, 0]).tolist(),
        np.array([0, 0, 1, 0]).tolist(),
        np.array([0, 0, 0, 1]).tolist()
    ]
    for i in range(4):
        vector = Vector(
            vector_embedding=embeddings[i],
            text=f"test {i}",
            metadata=Metadata(
                title=f"test {i}",
                author=f"test {i}",
                description=f"test {i}",
                keywords=[f"test {i}"],
                created_at=""
            ),
            parent_id=""
        )
        await vector_collection.insert_one(vector.model_dump())

    query_embedding = np.array([0, 0, 1, 0]).tolist()
    results = await nn_retriever.retrieve(query_embedding)
    assert results[0].text == "test 2"  # parallel to query embedding
