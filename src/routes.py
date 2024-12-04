from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import AsyncGenerator
from fastapi.datastructures import State
import logging
import os
import uvicorn
from src.database_handlers.database_handler import MongoDBHandler
from src.parsers.parser import AdvancedPDFParser
from typeguard import typechecked
from src.indexers.pdf_indexer import PDFIndexer
from src.chunkers.chunker import ApproximateChunkerWithOverlap
from src.embedders.dense_embedder import CohereDenseEmbedder
from dotenv import load_dotenv
import traceback
from bson import ObjectId
from src.models import (
    DeleteRequest, UploadResponse, GenerateRequest, GenerateResponse
)
from fastapi import UploadFile
from src.retrievers.dense_retriever import NNRetriever
from src.retrievers.retriever_pipeline import RetrieverPipeline
from src.agents.agent import RAGAgent
from src.retrievers.reranker import Reranker
from src.models import DeleteResponse
import asyncio
from typing import List


load_dotenv()

logging.basicConfig(level=logging.INFO)


class AppState(State):
    mongodb_client: AsyncIOMotorClient
    database: AsyncIOMotorDatabase


@typechecked
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.info("Connecting to MongoDB")
    app.state.mongodb_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    yield
    app.state.mongodb_client.close()


app = FastAPI(lifespan=lifespan)
app.state = AppState()


@typechecked
@app.post("/upload/")
async def upload_pdf(
    files: List[UploadFile],
    db_name: str
) -> List[UploadResponse]:
    responses = []
    try:
        async def process_file(file: UploadFile) -> UploadResponse:
            pdf_indexer = PDFIndexer(
                parser=AdvancedPDFParser(),
                chunker=ApproximateChunkerWithOverlap(
                    chunk_size=512,
                    chunk_overlap=128
                ),
                embedder=CohereDenseEmbedder(
                    api_key=os.getenv("COHERE_API_KEY", "")
                ),
                database_handler=MongoDBHandler(
                    client=app.state.mongodb_client,
                    db_name=db_name,
                    vector_collection_name="vectors",
                    doc_collection_name="documents"
                )
            )
            parent_document_id: str = await pdf_indexer.index_document(file)
            return UploadResponse(
                message="PDF uploaded successfully",
                document_id=parent_document_id
            )

        responses = await asyncio.gather(
            *(process_file(file) for file in files))
        return responses
    except Exception as e:
        logging.error("An error occurred:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# delete endpoint
@typechecked
@app.delete("/delete/")
async def delete_document(request: DeleteRequest) -> DeleteResponse:
    try:
        database_handler = MongoDBHandler(
            app.state.mongodb_client,
            db_name=request.db_name,
            vector_collection_name="vectors",
            doc_collection_name="documents"
        )
        await database_handler.delete_document(ObjectId(request.document_id))
        return DeleteResponse(
            message="Document deleted"
        )
    except Exception as e:
        logging.error("An error occurred:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@typechecked
@app.post("/generate/")
async def generate_answer(request: GenerateRequest) -> GenerateResponse:
    try:
        mongo_handler = MongoDBHandler(
            client=app.state.mongodb_client,
            db_name=request.db_name,
            vector_collection_name="vectors",
            doc_collection_name="documents"
        )
        agent = RAGAgent(
            retriever_pipeline=RetrieverPipeline(
                embedder=CohereDenseEmbedder(
                    api_key=os.getenv("COHERE_API_KEY", "")
                ),
                retriever=NNRetriever(
                    vector_collection=mongo_handler.vector_collection,
                ),
                reranker=Reranker(
                    cohere_api_key=os.getenv("COHERE_API_KEY", "")
                )
            ),
            mistral_api_key=os.getenv("MISTRAL_API_KEY", ""),
            model="mistral-large-latest"
        )
        response: GenerateResponse = await agent.chat(
            query=request.query,
        )
        return response
    except Exception as e:
        logging.error("An error occurred:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
