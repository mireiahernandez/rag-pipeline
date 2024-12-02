# abstract class for parsing
from abc import ABC, abstractmethod
from pdfminer.high_level import extract_text
from fastapi import UploadFile
from io import BytesIO

class BaseParser(ABC):
    @abstractmethod
    def extract_text(self, file: UploadFile) -> str:
        pass


class PDFParser(BaseParser):
    @staticmethod
    async def extract_text(file: UploadFile) -> str:
        text = extract_text(file)
        return text
