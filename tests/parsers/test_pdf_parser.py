import pytest
from starlette.datastructures import UploadFile
from io import BytesIO
from src.parsers.parser import AdvancedPDFParser
from src.models import Metadata


@pytest.fixture
def sample_pdf() -> BytesIO:
    pdf_content = b"%PDF-1.7\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000057 00000 n\n0000000111 00000 n\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n183\n%%EOF" # noqa E501
    return BytesIO(pdf_content)


@pytest.fixture
def sample_pdf_2() -> BytesIO:
    with open("examples/pdfs/ACME_Earnings.pdf", "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def sample_pdf_3() -> BytesIO:
    with open("examples/pdfs/Employee Handbook 2013-14.pdf", "rb") as file:
        return BytesIO(file.read())


@pytest.mark.asyncio
async def test_advanced_pdf_parser(sample_pdf: BytesIO) -> None:
    parser = AdvancedPDFParser()
    mock_file = UploadFile(filename="test.pdf", file=sample_pdf)
    bytes_io = await parser.convert_to_bytes(mock_file)
    text = await parser.extract_text(bytes_io)
    metadata = await parser.extract_metadata(bytes_io)
    assert isinstance(text, str)
    assert isinstance(metadata, Metadata)


@pytest.mark.asyncio
async def test_advanced_pdf_parser_2(sample_pdf_2: BytesIO) -> None:
    parser = AdvancedPDFParser()
    mock_file = UploadFile(filename="acme_earnings.pdf", file=sample_pdf_2)
    bytes_io = await parser.convert_to_bytes(mock_file)
    text = await parser.extract_text(bytes_io)
    metadata = await parser.extract_metadata(bytes_io)
    assert isinstance(text, str)
    assert isinstance(metadata, Metadata)


@pytest.mark.asyncio
async def test_advanced_pdf_parser_3(sample_pdf_3: BytesIO) -> None:
    parser = AdvancedPDFParser()
    mock_file = UploadFile(filename="human_resources.pdf", file=sample_pdf_3)
    bytes_io = await parser.convert_to_bytes(mock_file)
    text = await parser.extract_text(bytes_io)
    metadata = await parser.extract_metadata(bytes_io)
    assert isinstance(text, str)
    assert isinstance(metadata, Metadata)
