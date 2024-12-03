from src.database_handlers.database_handler import MongoDBHandler
import motor.motor_asyncio
import os
import pytest
from src.models import Document, Metadata
from dotenv import load_dotenv

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
    db_name = os.getenv("MONGO_TEST_DB_NAME")
    vector_collection_name = "vectors"
    doc_collection_name = "documents"
    return MongoDBHandler(
        mongodb_client,
        db_name,
        doc_collection_name=doc_collection_name,
        vector_collection_name=vector_collection_name
    )


@pytest.mark.asyncio
async def test_mongodb_handler_upload_document(mongodb_handler):
    # create test collection
    await mongodb_handler.doc_collection.delete_many({})

    document = Document(
        text="test",
        metadata=Metadata(
            title="test",
            author="test",
            description="test",
            keywords=["test"],
            created_at="2024-01-01"
        ),
        document_id="test"
    )

    document_id = await mongodb_handler.upload_document(document)

    print(document_id)
    # assert that the document was uploaded
    number_of_documents = await mongodb_handler.get_number_of_documents()
    assert number_of_documents == 1
    # empty the collection
    await mongodb_handler.doc_collection.delete_many({})
    # assert that the document was deleted
    number_of_documents = await mongodb_handler.get_number_of_documents()
    assert number_of_documents == 0


@pytest.mark.asyncio
async def test_mongodb_handler_delete_document(mongodb_handler):
    # insert a document
    document = Document(
        text="test",
        metadata=Metadata(
            title="test",
            author="test",
            description="test",
            keywords=["test"],
            created_at="2024-01-01"
        ),
        document_id="test"
    )
    inserted_id = await mongodb_handler.upload_document(document)
    number_of_documents = await mongodb_handler.get_number_of_documents()
    assert number_of_documents == 1
    await mongodb_handler.delete_document(inserted_id)
    # assert that the document was deleted
    number_of_documents = await mongodb_handler.get_number_of_documents()
    assert number_of_documents == 0
