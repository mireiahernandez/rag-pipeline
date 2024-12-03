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
