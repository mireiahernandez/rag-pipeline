from src.parsers.parser import BaseParser
from src.embedders.dense_embedder import BaseDenseEmbedder
from src.database_handlers.database_handler import (
    BaseDatabaseHandler
)
from abc import ABC, abstractmethod
from starlette.datastructures import UploadFile
from typeguard import typechecked
import logging
from src.models import (
    Metadata,
    Document,
    Vector,
)
from src.chunkers.chunker import BaseChunker
from starlette.responses import JSONResponse
from bson import ObjectId
from typing import List
from io import BytesIO


logging.basicConfig(level=logging.INFO)


class BaseIndexer(ABC):
    def __init__(
        self,
        parser: BaseParser,
        chunker: BaseChunker,
        embedder: BaseDenseEmbedder,
        database_handler: BaseDatabaseHandler
    ) -> None:
        self.parser = parser
        self.chunker = chunker
        self.embedder = embedder
        self.database_handler = database_handler

    @abstractmethod
    @typechecked
    async def index_document(self, file: UploadFile) -> JSONResponse:
        pass


@typechecked
class PDFIndexer(BaseIndexer):
    def __init__(
        self,
        parser: BaseParser,
        chunker: BaseChunker,
        embedder: BaseDenseEmbedder,
        database_handler: BaseDatabaseHandler
    ) -> None:
        """
        Indexer for PDF files.
        Handles parsing, embedding and uploading to database.
        """
        super().__init__(parser, chunker, embedder, database_handler)

    @typechecked
    async def index_document(self, file: UploadFile) -> JSONResponse:
        logging.info("Parsing PDF")
        filebytes: BytesIO = await self.parser.convert_to_bytes(file)

        logging.info("1. Extracting text from filebtyes object of type:"
                     f"{type(filebytes)}")
        text: str = await self.parser.extract_text(filebytes)
        metadata: Metadata = await self.parser.extract_metadata(filebytes)

        logging.info("2. Chunking text")
        chunks: List[str] = await self.chunker.chunk_text(text, metadata)
        logging.info("3. Embedding chunks: %s", chunks)
        embeddings: List[List[float]] = await self.embedder.embed_batch(
            chunks)

        logging.info("3. Uploading document to database")
        document: Document = Document(
            text=text,
            metadata=metadata
        )
        parent_document_id: ObjectId = \
            await self.database_handler.upload_document(document=document)
        parent_document_id_str: str = str(parent_document_id)

        logging.info("4. Uploading vectors to database")
        for i, embedding in enumerate(embeddings):
            vector: Vector = Vector(
                vector_embedding=embedding,
                metadata=metadata,
                parent_id=parent_document_id_str
            )
            _ = await self.database_handler.upload_vector(vector)
        return JSONResponse(
            content={
                "message": "PDF uploaded successfully",
                "document_id": parent_document_id_str
            },
            status_code=200
        )
