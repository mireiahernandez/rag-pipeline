from pydantic import BaseModel
from typing import List


class Metadata(BaseModel):
    title: str
    author: str
    description: str
    keywords: List[str]
    created_at: str


class Document(BaseModel):
    text: str
    metadata: Metadata


class Vector(BaseModel):
    vector_embedding: List[float]
    vector_id: str
    text: str
    metadata: Metadata
    parent_id: str


class DeleteRequest(BaseModel):
    document_id: str
    db_name: str


class GenerateRequest(BaseModel):
    query: str
    k: int = 10  # Number of similar documents to retrieve
    db_name: str


class UploadResponse(BaseModel):
    message: str
    document_id: str


class Query(BaseModel):
    query: str
    retrieved_ids: List[str]


class GenerateResponse(BaseModel):
    response: str
    queries: List[Query]
