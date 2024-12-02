# abstract class for parsing
from abc import ABC, abstractmethod
from pdfminer.high_level import extract_text
from starlette.datastructures import UploadFile
from io import BytesIO
from typing import Any, Dict
import fitz  # type: ignore
from typeguard import typechecked


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
    async def extract_metadata(self, file: BytesIO) -> Dict[str, Any]:
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
    async def extract_metadata(file: BytesIO) -> Dict[str, Any]:
        doc = fitz.open(stream=file.getvalue(), filetype="pdf")
        metadata: Dict[str, Any] = doc.metadata
        doc.close()
        return metadata


@typechecked
class PDFParser(BaseParser):
    @staticmethod
    @typechecked
    async def convert_to_bytes(file: UploadFile) -> BytesIO:
        file_bytes = await file.read()
        return BytesIO(file_bytes)

    @staticmethod
    @typechecked
    async def extract_text(bytes: BytesIO) -> str:
        text = extract_text(bytes)
        return text

    @staticmethod
    @typechecked
    async def extract_metadata(file: BytesIO) -> Dict[str, Any]:
        return {}
