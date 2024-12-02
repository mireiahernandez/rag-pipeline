import pytest
from src.parsers.parser import PDFParser, AdvancedPDFParser
from io import BytesIO


@pytest.mark.asyncio
async def test_pdf_parser():
    pdf_parser = PDFParser()
    pdf_path = "tests/routes/test.pdf"
    with open(pdf_path, "rb") as file:
        text = await pdf_parser.extract_text(file)
        print(text)
        assert len(text) > 1000


@pytest.mark.asyncio
async def test_advanced_pdf_parser():
    pdf_parser = AdvancedPDFParser()
    pdf_path = "tests/routes/test.pdf"
    with open(pdf_path, "rb") as file:
        bytesio = BytesIO(file.read())
        text = await pdf_parser.extract_text(bytesio)
        print(text)
        assert len(text) > 1000
        metadata = await pdf_parser.extract_metadata(bytesio)
        print(metadata)
        assert metadata is not None
