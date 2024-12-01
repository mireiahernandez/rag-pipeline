# test service response
import requests
import pytest
from io import BytesIO

@pytest.mark.asyncio
async def test_service_up():
    response = requests.get("http://0.0.0.0:8000/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.asyncio
async def test_upload_file_real():
    # load a pdf file
    pdf_path = "tests/routes/test.pdf"
    with open(pdf_path, "rb") as file:
        # Create the files dictionary as FastAPI expects
        files = {
            "file": ("hr_policy.pdf", file, "application/pdf")
        }
        response = requests.post("http://0.0.0.0:8000/uploadPDF/", files=files)
    print(response.json())
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_upload_file_dummy():
    files = {
        "file": ("test.pdf", BytesIO(b"fake PDF content"), "application/pdf")
    }
    response = requests.post("http://0.0.0.0:8000/uploadPDF/", files=files)
    print(response.json())
    assert response.status_code == 200
