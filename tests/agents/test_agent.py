from src.agents.agent import SimpleAgent, RAGAgent
import os
import pytest
from dotenv import load_dotenv
from src.embedders.dense_embedder import CohereDenseEmbedder
from src.retrievers.dense_retriever import NNRetriever
from src.retrievers.retriever_pipeline import RetrieverPipeline
from src.database_handlers.database_handler import MongoDBHandler
from src.retrievers.reranker import Reranker
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
    db_name = "test_tenant1"
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
def reranker() -> Reranker:
    return Reranker(
        cohere_api_key=os.getenv("COHERE_API_KEY")
    )


@pytest.fixture
def retriever_pipeline(embedder, retriever, reranker):
    return RetrieverPipeline(
        embedder=embedder,
        retriever=retriever,
        reranker=reranker
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
async def test_rag_agent_simple_question(rag_agent):
    response = await rag_agent.chat("What is the capital of France?")
    assert "paris" in response.response.lower()


@pytest.mark.asyncio
async def test_rag_agent_knowledge_question(rag_agent):
    response = await rag_agent.chat("How much was spent on R&D?")
    print(response)
    assert "300" in response.response.lower()
    assert "million" in response.response.lower()


@pytest.mark.asyncio
async def test_rag_agent_multiple_part_question(rag_agent):
    response = await rag_agent.chat(
        "How much was spent on R&D and what were the technological advancements?"  # noqa: E501
    )
    assert "300" in response.response.lower()
    assert "million" in response.response.lower()


@pytest.mark.asyncio
async def test_rag_agent_other_pdf_question(rag_agent):
    response = await rag_agent.chat(
        "What is the assault leave policy?"  # noqa: E501
    )
    print(response)
    assert "assault leave" in response.response.lower()
