# test service response
import requests
import pytest


@pytest.mark.asyncio
async def test_upload_endpoint() -> None:
    # load a pdf file
    pdf_path = "examples/pdfs/ACME_Earnings.pdf"
    with open(pdf_path, "rb") as file:
        # Create the files dictionary as FastAPI expects
        files = {
            "file": ("acme_earnings.pdf", file, "application/pdf")
        }
        # Add db_name as a parameter
        params = {
            "db_name": "test"  # Using test database for testing
        }
        response = requests.post(
            "http://0.0.0.0:8000/upload/",
            files=files,
            params=params
        )
    print(response.json())
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_endpoint() -> None:
    response = requests.delete(
        "http://0.0.0.0:8000/delete/",
        json={"document_id": "666666666666666666666666", "db_name": "test"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_generate_endpoint() -> None:
    response = requests.post(
        "http://0.0.0.0:8000/generate/",
        json={"query": "What is the capital of France?", "db_name": "test"}
    )
    assert response.status_code == 200
    assert "paris" in response.json()["response"].lower()
    print(response.json())
