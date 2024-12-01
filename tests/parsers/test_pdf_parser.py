import pytest
from src.parsers.parser import PDFParser


@pytest.mark.asyncio
async def test_pdf_parser():
    pdf_parser = PDFParser()
    pdf_path = "tests/routes/test.pdf"
    with open(pdf_path, "rb") as file:
        text = await pdf_parser.extract_text(file)
        print(text)
        assert len(text) > 1000
