from src.database_handlers.database_handler import MongoDBHandler
from pymongo import MongoClient
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

def test_mongodb_handler_upload_document():
    client = MongoClient(os.getenv("MONGODB_URI"))

    # create test collection
    mongodb_handler = MongoDBHandler(client, "testCollection", "pdfs")
    mongodb_handler.collection.delete_many({})

    # insert a document
    mongodb_handler.upload_document(text="test", metadata={"test": "test"})
    # assert that the document was uploaded
    assert mongodb_handler.collection.count_documents({}) == 1
    # empty the collection
    mongodb_handler.collection.delete_many({})
    # disconnect from client
    client.close()


def test_mongodb_handler_delete_document():
    client = MongoClient(os.getenv("MONGODB_URI"))
    # insert a document
    mongodb_handler = MongoDBHandler(client, "testCollection", "pdfs")
    document_id = str(uuid.uuid4())
    mongodb_handler.upload_document(text="test", metadata={"test": "test"}, document_id=document_id)
    # create test collection
    mongodb_handler.delete_document(document_id)
    # assert that the document was deleted
    assert mongodb_handler.collection.count_documents({}) == 0
    # disconnect from client
    client.close()
