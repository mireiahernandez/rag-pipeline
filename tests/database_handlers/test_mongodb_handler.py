from src.database_handlers.database_handler import MongoDBHandler
import motor.motor_asyncio
import os
import pytest


@pytest.mark.asyncio
async def test_mongodb_handler_upload_document():
    # use async client
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URI"))

    # create test collection
    mongodb_handler = MongoDBHandler(client, "testCollection", "pdfs")
    mongodb_handler.collection.delete_many({})

    # insert a document
    inserted_id = await mongodb_handler.upload_document(
        text="test", metadata={"test": "test"})
    print(inserted_id)
    # assert that the document was uploaded
    number_of_documents = await mongodb_handler.get_number_of_documents()
    assert number_of_documents == 1
    # empty the collection
    await mongodb_handler.collection.delete_many({})
    # assert that the document was deleted
    number_of_documents = await mongodb_handler.get_number_of_documents()
    assert number_of_documents == 0
    # disconnect from client
    client.close()


@pytest.mark.asyncio
async def test_mongodb_handler_delete_document():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    # insert a document
    mongodb_handler = MongoDBHandler(client, "testCollection", "pdfs")
    inserted_id = await mongodb_handler.upload_document(
        text="test", metadata={"test": "test"})
    number_of_documents = await mongodb_handler.get_number_of_documents()
    assert number_of_documents == 1
    await mongodb_handler.delete_document(inserted_id)
    # assert that the document was deleted
    number_of_documents = await mongodb_handler.get_number_of_documents()
    assert number_of_documents == 0
    client.close()
