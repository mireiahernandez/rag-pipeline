from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import AsyncGenerator
from fastapi.datastructures import State
import logging
import os
import uvicorn
from src.database_handlers.database_handler import MongoDBHandler
from src.parsers.parser import AdvancedPDFParser
from typeguard import typechecked


class AppState(State):
    mongodb_client: AsyncIOMotorClient
    database: AsyncIOMotorDatabase


@typechecked
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.info("Connecting to MongoDB")
    app.state.mongodb_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    app.state.database = app.state.mongodb_client["pdfCollection"]
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
        logging.info("Uploading PDF")
        mongodb_handler = MongoDBHandler(
            app.state.mongodb_client, "pdfCollection", "pdfs")

        logging.info("Converting to bytes")
        pdf_parser = AdvancedPDFParser()
        filebytes = await pdf_parser.convert_to_bytes(file)

        logging.info("Extracting text from filebtyes object of type:"
                     f"{type(filebytes)}")
        text = await pdf_parser.extract_text(filebytes)

        logging.info("Uploading to database")
        document_id = await mongodb_handler.upload_document(
            text=text, metadata={})

        return JSONResponse(
            content={
                "message": "PDF uploaded successfully",
                "document_id": document_id
            },
            status_code=200
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error uploading file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
