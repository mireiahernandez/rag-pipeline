from src.agents.agent import SimpleAgent, RAGAgent
import os
import pytest
from dotenv import load_dotenv
from src.embedders.dense_embedder import CohereDenseEmbedder
from src.retrievers.dense_retriever import NNRetriever
from src.retrievers.retriever_pipeline import RetrieverPipeline
from src.database_handlers.database_handler import MongoDBHandler
import motor.motor_asyncio

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
def simple_agent():
    return SimpleAgent(
        mistral_api_key=os.getenv("MISTRAL_API_KEY")
    )


@pytest.fixture
def embedder() -> CohereDenseEmbedder:
    return CohereDenseEmbedder(
        api_key=os.getenv("COHERE_API_KEY")
    )


@pytest.fixture
def retriever(vector_collection) -> NNRetriever:
    return NNRetriever(
        vector_collection=vector_collection
    )


@pytest.fixture
def retriever_pipeline(embedder, retriever):
    return RetrieverPipeline(
        embedder=embedder,
        retriever=retriever
    )


@pytest.fixture
def rag_agent(retriever_pipeline):
    return RAGAgent(
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        retriever_pipeline=retriever_pipeline
    )


@pytest.mark.asyncio
async def test_simple_agent(simple_agent):
    response = await simple_agent.chat("What is the capital of France?")
    assert "paris" in response.lower()


@pytest.mark.asyncio
async def test_rag_agent(rag_agent):
    response = await rag_agent.chat("What is the capital of France?")
    assert "paris" in response.lower()
