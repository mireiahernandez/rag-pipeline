import pytest
from starlette.datastructures import UploadFile
from io import BytesIO
from src.parsers.parser import AdvancedPDFParser, PDFParser


@pytest.fixture
def sample_pdf() -> BytesIO:
    pdf_content = b"%PDF-1.7\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000057 00000 n\n0000000111 00000 n\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n183\n%%EOF" # noqa E501
    return BytesIO(pdf_content)


@pytest.mark.asyncio
async def test_advanced_pdf_parser(sample_pdf: BytesIO) -> None:
    parser = AdvancedPDFParser()
    mock_file = UploadFile(filename="test.pdf", file=sample_pdf)
    bytes_io = await parser.convert_to_bytes(mock_file)
    text = await parser.extract_text(bytes_io)
    metadata = await parser.extract_metadata(bytes_io)
    assert isinstance(text, str)
    assert isinstance(metadata, dict)


@pytest.mark.asyncio
async def test_pdf_parser(sample_pdf: BytesIO) -> None:
    parser = PDFParser()
    mock_file = UploadFile(filename="test.pdf", file=sample_pdf)
    bytes_io = await parser.convert_to_bytes(mock_file)
    text = await parser.extract_text(bytes_io)
    metadata = await parser.extract_metadata(bytes_io)
    assert isinstance(text, str)
    assert isinstance(metadata, dict)
