from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi import UploadFile
import os
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from src.database_handlers.database_handler import MongoDBHandler
from src.parsers.parser import AdvancedPDFParser
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import AsyncGenerator
from fastapi.datastructures import State

# Configure the logger to output INFO level logs to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")


# Define a custom state class
class AppState(State):
    mongodb_client: AsyncIOMotorClient
    database: AsyncIOMotorDatabase


# connect to MongoDB with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.info("Connecting to MongoDB")
    app.state.mongodb_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    logging.info("Connected to MongoDB")
    app.state.database = app.state.mongodb_client["pdfCollection"]
    logging.info("Connected to database")
    yield
    app.state.mongodb_client.close()


# Create the FastAPI app with typed state
app = FastAPI(lifespan=lifespan)
app.state = AppState()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload/")
async def upload_pdf(file: UploadFile):
    # return await db.upload_pdf(file)
    try:
        logging.info("Uploading PDF")
        mongodb_handler = MongoDBHandler(
            app.state.mongodb_client, "pdfCollection", "pdfs")
        logging.info("Converting to bytes")
        pdf_parser = AdvancedPDFParser()
        filebytes = await pdf_parser.convert_to_bytes(file)
        logging.info(
            f"Extracting text from filebtyes object of type: {type(filebytes)}"
        )
        text = await pdf_parser.extract_text(filebytes)
        logging.info("Uploading to database")
        document_id = await mongodb_handler.upload_document(
            text=text, metadata={})
        return JSONResponse(
            content={
                "message": "PDF uploaded successfully",
                "document_id": document_id},
            status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error uploading file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
