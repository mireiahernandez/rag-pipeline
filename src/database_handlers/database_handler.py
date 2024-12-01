# abstract class for database handler
from abc import ABC, abstractmethod
from pymongo import MongoClient
import uuid

class BaseDatabaseHandler(ABC):
    @abstractmethod
    def upload_document(self, metadata: dict, text: str):
        pass

    @abstractmethod
    def delete_document(self, document_id: str):
        pass


class MongoDBHandler(BaseDatabaseHandler):
    def __init__(self, client: MongoClient, db_name: str, collection_name: str):
        self.client = client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def upload_document(self, metadata: dict, text: str, document_id: str = None):
        document = {
            "metadata": metadata,
            "text": text,
            "_id": document_id if document_id else str(uuid.uuid4())
        }
        self.collection.insert_one(document)

    def delete_document(self, document_id: str):
        self.collection.delete_one({"_id": document_id})
