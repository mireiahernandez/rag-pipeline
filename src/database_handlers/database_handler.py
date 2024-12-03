# abstract class for database handler
from abc import ABC, abstractmethod
import motor.motor_asyncio
from typeguard import typechecked  # type: ignore
from pymongo.results import InsertOneResult
from src.models import Document, Vector
from bson import ObjectId


class BaseDatabaseHandler(ABC):
    @abstractmethod
    async def upload_document(
        self,
        document: Document
    ) -> ObjectId:
        pass

    @abstractmethod
    async def delete_document(
        self,
        document_id: ObjectId
    ) -> None:
        pass

    @abstractmethod
    async def upload_vector(
        self,
        vector: Vector
    ) -> ObjectId:
        pass

    @abstractmethod
    async def delete_vector(
        self,
        vector_id: ObjectId
    ) -> None:
        pass


@typechecked
class MongoDBHandler(BaseDatabaseHandler):
    @typechecked
    def __init__(
        self,
        client: motor.motor_asyncio.AsyncIOMotorClient,
        db_name: str,
        doc_collection_name: str,
        vector_collection_name: str
    ):
        self.client: motor.motor_asyncio.AsyncIOMotorClient = client
        self.db: motor.motor_asyncio.AsyncIOMotorDatabase = \
            self.client[db_name]
        self.doc_collection: motor.motor_asyncio.AsyncIOMotorCollection = \
            self.db[doc_collection_name]
        self.vector_collection: motor.motor_asyncio.AsyncIOMotorCollection = \
            self.db[vector_collection_name]

    @typechecked
    async def upload_document(
        self,
        document: Document,
    ) -> ObjectId:
        """
        Upload a document to the database
        """
        created_document: InsertOneResult = await self.doc_collection.insert_one( # noqa E501
            document.model_dump())
        inserted_id: ObjectId = created_document.inserted_id
        return inserted_id

    @typechecked
    async def upload_vector(
        self,
        vector: Vector
    ) -> ObjectId:
        """
        Upload a vector embedding to the database
        """
        created_vector: InsertOneResult = await self.vector_collection.insert_one( # noqa E501
            vector.model_dump())
        inserted_id: ObjectId = created_vector.inserted_id
        return inserted_id

    @typechecked
    async def delete_document(
        self,
        document_id: ObjectId
    ) -> None:
        """
        Delete a document from the database
        """
        await self.doc_collection.delete_one({"_id": document_id})

    @typechecked
    async def delete_vector(
        self,
        document_id: ObjectId
    ) -> None:
        """
        Delete a document from the database
        """
        await self.vector_collection.delete_one({"_id": document_id})

    @typechecked
    async def get_number_of_documents(self) -> int:
        """
        Get the number of documents in the database
        """
        return await self.doc_collection.count_documents({})
