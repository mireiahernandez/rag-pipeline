from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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
from src.models import DeleteRequest
from fastapi import UploadFile
from src.models import GenerateRequest
from src.retrievers.dense_retriever import NNRetriever
from src.retrievers.retriever_pipeline import RetrieverPipeline
from src.agents.agent import RAGAgent

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
@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@typechecked
@app.post("/upload/")
async def upload_pdf(file: UploadFile) -> JSONResponse:
    try:
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
                app.state.mongodb_client,
                db_name=os.getenv("MONGO_DB_TENANT_DB_NAME", "tenant1"),
                vector_collection_name="vectors",
                doc_collection_name="documents"
            )
        )
        response: JSONResponse = await pdf_indexer.index_document(file)
        return response
    except Exception as e:
        # print also the traceback in a pretty format
        logging.error("An error occurred:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# delete endpoint
@typechecked
@app.delete("/delete/")
async def delete_document(request: DeleteRequest) -> JSONResponse:
    try:
        database_handler = MongoDBHandler(
            app.state.mongodb_client,
            db_name=request.db_name,
            vector_collection_name="vectors",
            doc_collection_name="documents"
        )
        await database_handler.delete_document(ObjectId(request.document_id))
        return JSONResponse(
            status_code=200,
            content={"message": "Document deleted"})
    except Exception as e:
        logging.error("An error occurred:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@typechecked
@app.post("/generate/")
async def generate_answer(request: GenerateRequest) -> JSONResponse:
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

            ),
            mistral_api_key=os.getenv("MISTRAL_API_KEY", ""),
            model="mistral-large-latest"
        )
        response = await agent.chat(
            query=request.query,
        )
        return JSONResponse(
            status_code=200,
            content={"message": response}
        )
    except Exception as e:
        logging.error("An error occurred:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
