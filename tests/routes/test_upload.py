# test service response
import requests
import pytest
from io import BytesIO
from typing import Dict


@pytest.mark.asyncio
async def test_service_up() -> None:
    response = requests.get("http://0.0.0.0:8000/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_upload_file_real() -> None:
    # load a pdf file
    pdf_path = "tests/routes/test.pdf"
    with open(pdf_path, "rb") as file:
        # Create the files dictionary as FastAPI expects
        files = {
            "file": ("new_hr_policy.pdf", file, "application/pdf")
        }
        response = requests.post("http://0.0.0.0:8000/upload/", files=files)
    print(response.json())
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_upload_file_dummy() -> None:
    # Create minimal valid PDF content
    pdf_content = b"%PDF-1.7\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000057 00000 n\n0000000111 00000 n\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n183\n%%EOF" # noqa E501

    files: Dict[str, tuple[str, BytesIO, str]] = {
        "file": ("test.pdf", BytesIO(pdf_content), "application/pdf")
    }
    response = requests.post("http://0.0.0.0:8000/upload/", files=files)
    print(response.json())
    assert response.status_code == 200
