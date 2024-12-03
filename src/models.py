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
    metadata: Metadata
    parent_id: str
