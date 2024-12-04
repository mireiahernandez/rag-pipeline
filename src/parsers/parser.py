# abstract class for parsing
from abc import ABC, abstractmethod
from starlette.datastructures import UploadFile
from io import BytesIO
from typing import Any, Dict
import fitz  # type: ignore
from typeguard import typechecked
from src.models import Metadata


@typechecked
class BaseParser(ABC):
    @abstractmethod
    @typechecked
    async def convert_to_bytes(self, file: UploadFile) -> BytesIO:
        pass

    @abstractmethod
    @typechecked
    async def extract_text(self, file: BytesIO) -> str:
        pass

    @abstractmethod
    @typechecked
    async def extract_metadata(self, file: BytesIO) -> Metadata:
        pass


@typechecked
class AdvancedPDFParser(BaseParser):
    @staticmethod
    @typechecked
    async def convert_to_bytes(file: UploadFile) -> BytesIO:
        file_bytes = await file.read()
        return BytesIO(file_bytes)

    @staticmethod
    @typechecked
    async def extract_text(filebytes: BytesIO) -> str:
        doc = fitz.open(stream=filebytes.getvalue(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    @staticmethod
    @typechecked
    async def extract_metadata(file: BytesIO) -> Metadata:
        doc = fitz.open(stream=file.getvalue(), filetype="pdf")
        metadata: Dict[str, Any] = doc.metadata
        metadata_pyd = Metadata(
            created_at=metadata.get("creationDate", ""),
            keywords=metadata.get("keywords", "").split(),
            title=metadata.get("title", ""),
            author=metadata.get("author", ""),
            description=metadata.get("subject", "")
        )
        return metadata_pyd
