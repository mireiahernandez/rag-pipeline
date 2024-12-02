# abstract class for parsing
from abc import ABC, abstractmethod
from pdfminer.high_level import extract_text
from fastapi import UploadFile
from io import BytesIO
import fitz  # type: ignore


class BaseParser(ABC):
    @abstractmethod
    async def convert_to_bytes(self, file: UploadFile) -> BytesIO:
        pass

    @abstractmethod
    async def extract_text(self, file: BytesIO) -> str:
        pass

    @abstractmethod
    async def extract_metadata(self, file: BytesIO) -> dict:
        pass


class AdvancedPDFParser(BaseParser):
    @staticmethod
    async def convert_to_bytes(file: UploadFile) -> BytesIO:
        file_bytes = await file.read()
        return BytesIO(file_bytes)

    @staticmethod
    async def extract_text(filebytes: BytesIO) -> str:
        doc = fitz.open(stream=filebytes.getvalue(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    @staticmethod
    async def extract_metadata(file: BytesIO) -> dict:
        doc = fitz.open(stream=file.getvalue(), filetype="pdf")
        metadata = doc.metadata
        doc.close()
        return metadata


class PDFParser(BaseParser):
    @staticmethod
    async def convert_to_bytes(file: UploadFile) -> BytesIO:
        file_bytes = await file.read()
        return BytesIO(file_bytes)

    @staticmethod
    async def extract_text(bytes: BytesIO) -> str:
        text = extract_text(bytes)
        return text

    @staticmethod
    async def extract_metadata(file: BytesIO) -> dict:
        return {}
