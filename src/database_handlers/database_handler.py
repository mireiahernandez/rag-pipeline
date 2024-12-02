# abstract class for database handler
from abc import ABC, abstractmethod
import uuid
from typing import Optional
import motor.motor_asyncio
from typeguard import typechecked  # type: ignore
from pymongo.results import InsertOneResult


class BaseDatabaseHandler(ABC):
    @abstractmethod
    async def upload_document(
        self,
        metadata: dict,
        text: str,
        document_id: Optional[str] = None
    ) -> str:
        pass

    @abstractmethod
    async def delete_document(self, document_id: str) -> None:
        pass


@typechecked
class MongoDBHandler(BaseDatabaseHandler):
    @typechecked
    def __init__(
        self,
        client: motor.motor_asyncio.AsyncIOMotorClient,
        db_name: str,
        collection_name: str
    ):
        self.client = client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    @typechecked
    async def upload_document(
        self,
        metadata: dict,
        text: str,
        document_id: Optional[str] = None
    ) -> str:
        """
        Upload a document to the database
        """
        document = {
            "metadata": metadata,
            "text": text,
            "_id": document_id if document_id else str(uuid.uuid4())
        }
        created_document: InsertOneResult = await self.collection.insert_one(
            document)
        inserted_id: str = created_document.inserted_id
        return inserted_id

    @typechecked
    async def delete_document(
        self,
        document_id: str
    ) -> None:
        """
        Delete a document from the database
        """
        await self.collection.delete_one({"_id": document_id})

    @typechecked
    async def get_number_of_documents(self) -> int:
        """
        Get the number of documents in the database
        """
        return await self.collection.count_documents({})
