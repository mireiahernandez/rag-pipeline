from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi import UploadFile
from pymongo import MongoClient
import os
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from src.database_handlers.database_handler import MongoDBHandler
from src.parsers.parser import PDFParser
import motor.motor_asyncio

# connect to MongoDB with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    yield
    app.mongodb_client.close()


app = FastAPI(lifespan=lifespan)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload/")
async def upload_pdf(file: UploadFile):
    # return await db.upload_pdf(file)
    try:
        mongodb_handler = MongoDBHandler(app.mongodb_client, "pdfCollection", "pdfs")
        pdf_parser = PDFParser()
        # text = await pdf_parser.extract_text(file)
        text = "test"
        mongodb_handler.upload_document(text=text, metadata={})
        return JSONResponse(content={"message": f"PDF uploaded successfully"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)